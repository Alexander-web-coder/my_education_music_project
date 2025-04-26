from fastapi import APIRouter, status, Depends
from sqlmodel import Session, select, text
from app.db import  get_session
from app.models.models import Track as Track_db
from app.shemas.tracks import Track


router = APIRouter(prefix="/tracks", tags=["Операции с треками"])

# для теста базы
@router.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(session: Session = Depends(get_session)):
    result = session.exec(select(text("'Hello world'"))).all()
    return result


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list(session: Session = Depends(get_session)):  #TODO
    result = session.exec(select(Track_db)).all()
    return result


@router.post("/create_track", status_code=status.HTTP_201_CREATED)
def create_track(track: Track, session: Session = Depends(get_session)):
    new_track = Track_db(
        title = track.title,
        author = track.author,
        genre = track.genre
    )
    session.add(new_track)
    session.commit()
    session.refresh(new_track)
    return track


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
def delete_track():  #TODO
    pass
