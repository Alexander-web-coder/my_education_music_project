from fastapi import APIRouter, status, Depends
from sqlmodel import Session, select, text
from app.db import  get_session


router = APIRouter(prefix="/tracks", tags=["Операции с треками"])

# для теста базы
@router.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(session: Session = Depends(get_session)):
    result = session.exec(select(text("'Hello world'"))).all()
    return result


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list():  #TODO
    pass


@router.post("/create_track", status_code=status.HTTP_201_CREATED)
def create_track():  #TODO
    pass


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
def delete_track():  #TODO
    pass
