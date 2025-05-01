#from http.client import HTTPException

from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlmodel import Session, select, delete, text
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, InternalError, IntegrityError
from app.db import  get_session
from app.models.models import Track as Track_db, Ratings
from app.schemas.schemas_obj import Track, DeleteTrack
#from app.main import app


router = APIRouter(prefix="/tracks", tags=["Операции с треками"])

# @app.exception_handler(SQLAlchemyError)
# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     # Для ошибок целостности (например, дублирование уникального ключа)
#     return JSONResponse(
#             status_code=400,
#             content={"message": "Возможно, запись уже существует или нарушены ограничения базы данных"},
#         )


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list(session: Session = Depends(get_session)):
    """Возвращает полный лист треков"""
    result = session.exec(select(Track_db)).all()
    return result


@router.post("/create_track", status_code=status.HTTP_201_CREATED)
def create_track(track: Track, session: Session = Depends(get_session)):
    """Создает запись о треке"""
    new_track = Track_db(
        title = track.title,
        author = track.author,
        genre = track.genre
    )
    try:
        session.add(new_track)
        session.commit()
        session.refresh(new_track)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Комбинация трек\автор должна быть уникальной.")
    return new_track


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
#def delete_track(track_id: DeleteTrack, session: Session = Depends(get_session)):
def delete_track(track_id: int, session: Session = Depends(get_session)):
    """Кскадно удаляет запись о треке и его оценках. """
    # for_delete = session.exec(select(Track_db).where(Track_db.id == track_id.id))
    #stmt = select(Track_db).where(Track_db.id == track_id.id)
    # stmt_track = select(Track_db).where(Track_db.id == track_id)
    #stmt_rating = select(Ratings).where(Ratings.track_id == track_id)
    try:
        # удаляем все оценки трека. Если он не существует, ошибка не возникнет!
        stmt_rating = delete(Ratings).where(Ratings.track_id == track_id)
        session.exec(stmt_rating)
        session.commit()
        # удаляем трек из таблицы треков. Если его нет - ошибка возникнет!
        stmt_track = select(Track_db).where(Track_db.id == track_id)
        for_delete = session.exec(stmt_track).one()
        # for_delete = results.one()
        session.delete(for_delete)
        session.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Трека не существует.")

    # return for_delete
    # return results
    return  for_delete


