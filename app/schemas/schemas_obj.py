"""Модели для ФастАПИ(не для базы!)"""
from pydantic import BaseModel, Field, EmailStr


class Track(BaseModel):
    """Трек для веб-интерфейса"""
    title: str = Field(max_length=80)
    author: str = Field(max_length=100)
    genre: str = None


class User(BaseModel):
    """Пользователь для веб-интерфейса"""
    login: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = Field(default=None)


class Ratings(BaseModel):
    """Оценка трека для веб-интерфейса"""
    #hash: str
    track_id: int
    estimate: int = Field(ge=1, le=5)


class Token(BaseModel):
    """Токен для веб-интерфейса"""
    access_token: str
    token_type: str
