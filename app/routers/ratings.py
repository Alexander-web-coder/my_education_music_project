"""Модуль для операций с оценками (рейтингом)"""
from typing import List, Callable
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, func, and_
from app.db import get_session
from app.core.security import get_current_user
from app.schemas.schemas_obj import Ratings
from app.models.models import Ratings as Rating_db, Track

func: Callable

router = APIRouter(prefix="/ratings", tags=["Операции с оценками"])

@router.patch("/set_rating", status_code=status.HTTP_201_CREATED) #TODO
def set_rating(rating: Ratings, login=Depends(get_current_user), session=Depends(get_session)) -> Rating_db:
    """Устанавливает оценку трека, требуется логин юзера"""
    # statement = select(User).where(User.login == login.login)
    # user_exist_id = session.exec(statement).first()
    new_rating = Rating_db(
        # user_id  = user_exist_id.id,
        user_id = login.id,
        track_id = rating.track_id,
        estimate = rating.estimate
    )
    try:
        session.add(new_rating)
        session.commit()
        session.refresh(new_rating)
    except SQLAlchemyError as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Трека не существует."
            ) from _
    return new_rating



@router.patch("/change_rating", status_code=status.HTTP_201_CREATED)
def change_rating(rating: Ratings, login=Depends(get_current_user), session=Depends(get_session)): # -> Rating_db:
    """Меняет оценку трека, требуется логин юзера"""
    # statement = select(User).where(User.login == login.login)
    # user_exist_id = session.exec(statement).first()
    # new_rating = Rating_db(
    #     # user_id  = user_exist_id.id,
    #     user_id = login.id,
    #     track_id = rating.track_id,
    #     estimate = rating.estimate
    # )
    stmt = select(Rating_db).where(and_(
        Rating_db.user_id == login.id,
        Rating_db.track_id == rating.track_id))
    # new_rating = session.scalars(stmt).one()
    # new_rating = session.exec(stmt).all()
    # if new_rating == []:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Оценки не существует. Для создания оценки воспользуйтесь /set_rating."
    #     )

    # stmt = select(Rating_db).where(and_(
    #     Rating_db.user_id == login.id,
    #     Rating_db.track_id == rating.track_id))
    try:
        new_rating = session.scalars(stmt).one()
        new_rating.estimate = rating.estimate
        session.commit()
        session.refresh(new_rating)
    except SQLAlchemyError as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Оценки не существует. Для создания оценки воспользуйтесь /set_rating."
            ) from _
    return new_rating

@router.get("/get_my_recommend", status_code=status.HTTP_200_OK)
def get_my_recommend(user_id: int, session: Session = Depends(get_session)) -> List[Track]:
    """Возвращает список рекомендованных треков для указанного юзера"""

    # Получаем любимые жанры юзера
    stmt = (
        select(Track.genre)
        .join(Rating_db, Rating_db.track_id == Track.id)
        .where(and_(
            Rating_db.user_id == user_id,
            Rating_db.estimate >= 4
        ))
        .group_by(Track.genre)
        .order_by(func.count().desc())
        .limit(2)
    )
    user_genres = list(session.exec(stmt).all())

    if not user_genres:
        return []

    #  Находим похожих юзеров(высоко оценили треки этих жанров)
    stmt = (
        select(Rating_db.user_id)
        .join(Track, Track.id == Rating_db.track_id)
        .where(and_(
        Rating_db.user_id != user_id,
            Rating_db.estimate >= 4,
            Track.genre.in_(user_genres)
        ))
        .group_by(Rating_db.user_id)
        .having(func.count() >= 2)
    )
    similar_users = list(session.exec(stmt).all())

    if not similar_users:
        return []

    # Получаем треки, которые высоко оценили похожие юзеры
    stmt = (select(Track).join(Rating_db, Rating_db.track_id == Track.id).where(
        and_(Rating_db.user_id.in_(similar_users), # pylint: disable=no-member
             Rating_db.estimate >= 4, Track.genre.in_(user_genres))).group_by(
            Track.id))

    # Находим треки, которые юзер уже оценил
    rated_tracks =list(session.exec(
        select(Rating_db.track_id)
        .where(Rating_db.user_id == user_id)
    ).all())

    # Исключаем оцененные треки
    if rated_tracks:
        stmt = stmt.where(Track.id.not_in(rated_tracks)) # pylint: disable=no-member

    # Сортируем и ограничиваем результат
    stmt = (
        stmt.order_by(
            func.count().desc(),
            func.avg(Rating_db.estimate).desc()
        )
        .limit(3)
    )

    return session.exec(stmt).all()

# def get_my_recommend(login=Depends(get_current_user), session=Depends(get_session)):
# def get_music_recommendations(user_id: int, session: Session = Depends(get_session)) -> List[Track]:
# def get_music_recommendations(user_id: int, session: Session = Depends(get_session)):
#     """Возвращает список рекомендованных треков """
#
#     # 1. Определяем 2 самых любимых жанра
#     user_genres_subq = (
#         select(Track.genre)
#         .join(Rating_db, Rating_db.track_id == Track.id)
#         .where(and_(
#             Rating_db.user_id == user_id,
#             Rating_db.estimate >= 4
#         ))
#         .group_by(Track.genre)
#         .order_by(func.count().desc())
#         .limit(2)
#         .subquery()
#     )
#
#     # 2. Находим ID
#     similar_users_subq = (
#         select(Rating_db.user_id)
#         .join(Track, Track.id == Rating_db.track_id)
#         .where(and_(
#             Rating_db.user_id != user_id,
#             Rating_db.estimate >= 4,
#             Track.genre.in_(select(user_genres_subq.c.genre))
#         ))
#         .group_by(Rating_db.user_id)
#         .having(func.count() >= 2)
#         .subquery()
#     )
#
#     # 3. Получаем рекомендации треков
#     recommendations = session.exec(
#         select(Track)
#         .join(Rating_db, Rating_db.track_id == Track.id)
#         .where(and_(
#             Rating_db.user_id.in_(select(similar_users_subq.c.user_id)),
#             Rating_db.estimate >= 4,
#             Track.genre.in_(select(user_genres_subq.c.genre)),
#             not_(exists(
#                 select(Rating_db.id)
#                 .where(and_(
#                     Rating_db.user_id == user_id,
#                     Rating_db.track_id == Track.id
#                 ))
#             ))
#         ))
#         .group_by(Track.id)
#         .order_by(
#             func.count().desc(),
#             func.avg(Rating_db.estimate).desc()
#         )
#         .limit(3)
#     ).all()
#
#     # return recommendations
#     return None
