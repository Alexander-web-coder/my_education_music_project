"""Модуль для операций с треками"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select, delete
from sqlalchemy.exc import SQLAlchemyError
from app.db import  get_session
from app.models.models import Track as Track_db, Ratings
from app.schemas.schemas_obj import Track
from app.core.security import get_current_user



router = APIRouter(prefix="/tracks", tags=["Операции с треками"])


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list(session: Session = Depends(get_session)) -> list[Track_db]:
    """Возвращает полный лист треков"""
    result = session.exec(select(Track_db)).all()
    return result


@router.post("/create_track", status_code=status.HTTP_201_CREATED)
def create_track(track: Track, session: Session = Depends(get_session),
                 _ = Depends(get_current_user)) -> Track_db:
    """Создает запись о треке. Требуется авторизация."""
    new_track = Track_db(
        title = track.title,
        author = track.author,
        genre = track.genre
    )
    try:
        session.add(new_track)
        session.commit()
        session.refresh(new_track)
    except SQLAlchemyError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Комбинация трек-автор должна быть уникальной.") from _
    return new_track


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(track_id: int, session: Session = Depends(get_session),
                 _ = Depends(get_current_user)):
    """Каскадно удаляет запись о треке и его оценках. Требуется авторизация. """
    try:
        # удаляем все оценки трека. Если он не существует, ошибка не возникнет!
        stmt_rating = delete(Ratings).where(Ratings.track_id == track_id)
        session.exec(stmt_rating)
        session.commit()
        # удаляем трек из таблицы треков. Если его нет - ошибка возникнет!
        stmt_track = select(Track_db).where(Track_db.id == track_id)
        for_delete = session.exec(stmt_track).one()
        session.delete(for_delete)
        session.commit()
    except SQLAlchemyError as _:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Трек не существует.") from _
    return  for_delete
