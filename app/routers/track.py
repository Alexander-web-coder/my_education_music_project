#from http.client import HTTPException

from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlmodel import Session, select, text
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, InternalError, IntegrityError
from app.db import  get_session
from app.models.models import Track as Track_db
from app.schemas.tracks import Track, DeleteTrack
#from app.main import app


router = APIRouter(prefix="/tracks", tags=["Операции с треками"])

# @app.exception_handler(SQLAlchemyError)
# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     # Для ошибок целостности (например, дублирование уникального ключа)
#     return JSONResponse(
#             status_code=400,
#             content={"message": "Возможно, запись уже существует или нарушены ограничения базы данных"},
#         )

# для теста базы
@router.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(session: Session = Depends(get_session)):
    result = session.exec(select(text("'Hello world'"))).all()
    return result


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list(session: Session = Depends(get_session)):
    result = session.exec(select(Track_db)).all()
    return result


@router.post("/create_track", status_code=status.HTTP_201_CREATED)
def create_track(track: Track, session: Session = Depends(get_session)):
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
        # raise HTTPException(status_code=status.HTTP_100_CONTINUE,
        #                     detail="Ошибка записи в базу. Возможно, оценка уже поставлена.")
        raise

    return track


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(track_id: DeleteTrack, session: Session = Depends(get_session)):
    # for_delete = session.exec(select(Track_db).where(Track_db.id == track_id.id))
    stmt = select(Track_db).where(Track_db.id == track_id.id)
    results = session.exec(stmt)
    for_delete = results.one()
    session.delete(for_delete)
    session.commit()
    return for_delete


