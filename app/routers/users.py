from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import  select
from app.db import  get_session
from app.models.models import User
from core.security import hash_password, verify_password, create_access_token
from app.schemas.tracks import Token

router = APIRouter(prefix="/users", tags=["Операции с пользователями"])

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(login: str, password: str, session = Depends(get_session)):
    """Создает нового пользователя"""
    user_exists = session.exec(select(User).where(User.login == login)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user = User(login=login, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    return {"message": "Пользователь зарегистрирован"}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session = Depends(get_session)):
    """Аутентифицирует пользователя, возвращает токен"""
    user = session.exec(select(User).where(User.login == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}
