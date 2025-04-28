from fastapi import APIRouter, status, Depends
from sqlmodel import  select
from app.db import get_session
from core.security import get_current_user
from app.schemas.tracks import Ratings
from app.models.models import Ratings as Rating_db, User

router = APIRouter(prefix="/ratings", tags=["Операции с оценками"])

@router.patch("/set_rating", status_code=status.HTTP_201_CREATED)
def set_rating(rating: Ratings, login=Depends(get_current_user), session=Depends(get_session)):
    statement = select(User).where(User.login == login.login)
    user_exist_id = session.exec(statement).first()
    new_rating = Rating_db(
        user_id  = user_exist_id.id,
        track_id = rating.track_id,
        estimate = rating.estimate
    )
    session.add(new_rating)
    session.commit()
    session.refresh(new_rating)
    return new_rating



@router.get("/get_top", status_code=status.HTTP_200_OK)
def get_top():  #TODO
    pass

@router.get("/get_my_recommend", status_code=status.HTTP_200_OK)
def get_my_recommend():  #TODO
    pass