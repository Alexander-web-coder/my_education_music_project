"""Модели для ФастАПИ(не для базы!)"""
from pydantic import BaseModel, Field

class Track(BaseModel):
    """Трек"""
    title: str
    author: str
    genre: str = None


class User(BaseModel):
    """Пользователь"""
    login: str
    password: str
    # first_name: str
    # last_name: str
    #hash: str надо подумать


class Ratings(BaseModel):
    """Оценка трека"""
    #hash: str
    track_id: int
    estimate: int = Field(gt=0, lt=6)

# class DeleteTrack(BaseModel):
#     id: int

class Token(BaseModel):
    """Токен"""
    access_token: str
    token_type: str
