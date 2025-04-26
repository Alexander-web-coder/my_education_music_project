from markdown_it.rules_block import table
from pygments.lexer import default
from sqlmodel import SQLModel, Field as SQLField


class Track(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    title: str
    author: str
    genre: str

class User(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    first_name: str
    last_name: str
    email: str = SQLField(default=None)
    hashed_password: str

class Ratings(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    user_id: int = SQLField(default=None, nullable=False, foreign_key="user.id")
    track_id: int = SQLField(default=None, nullable=False, foreign_key="track.id")
    estimate: int = SQLField(gt=1, le=10)
