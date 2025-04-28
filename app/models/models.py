from markdown_it.rules_block import table
from pygments.lexer import default
from sqlmodel import SQLModel, Field as SQLField, UniqueConstraint


class Track(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    title: str
    author: str
    genre: str

class User(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    login: str = SQLField(unique=True)
    first_name: str = SQLField(default=None, nullable=True)
    last_name: str = SQLField(default=None, nullable=True)
    email: str = SQLField(default=None, nullable=True)
    hashed_password: str

class Ratings(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('user_id', 'track_id', name='user_and_track_constraint'),
    )

    id: int = SQLField(default=None, nullable=False, primary_key=True)
    user_id: int = SQLField(default=None, nullable=False, foreign_key="user.id")
    track_id: int = SQLField(default=None, nullable=False, foreign_key="track.id")
    estimate: int = SQLField(gt=0, le=6)
