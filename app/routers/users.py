from fastapi import APIRouter, status, Depends
from sqlmodel import  select
from app.db import  get_session
from app.models.models import User
from core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Операции с пользователями"])

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(login: str, password: str, session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.login==login)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user = User(login=login, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    return {"message": "Пользователь зарегистрирован"}

@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(): #TODO
    pass