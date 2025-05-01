"""Описание структуры таблиц"""

from sqlmodel import SQLModel, Field as SQLField, UniqueConstraint


class Track(SQLModel, table=True):
    """Модель треков для базы"""
    __table_args__ = (
        UniqueConstraint('title', 'author', name='track_and_author_constraint'),
    )
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    title: str
    author: str
    genre: str

class User(SQLModel, table=True):
    """Модель пользователя для базы"""
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    login: str = SQLField(unique=True)
    first_name: str = SQLField(default=None, nullable=True)
    last_name: str = SQLField(default=None, nullable=True)
    email: str = SQLField(default=None, nullable=True)
    hashed_password: str

class Ratings(SQLModel, table=True):
    """Модель рейтинга для базы"""
    __table_args__ = (
        UniqueConstraint('user_id', 'track_id', name='user_and_track_constraint'),
    )

    id: int = SQLField(default=None, nullable=False, primary_key=True)
    user_id: int = SQLField(default=None, nullable=False, foreign_key="user.id")
    track_id: int = SQLField(default=None, nullable=False, foreign_key="track.id")
    estimate: int = SQLField(ge=1, le=5)
