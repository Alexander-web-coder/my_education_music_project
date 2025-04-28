from dataclasses import Field

from pydantic import BaseModel, Field

class Track(BaseModel): #TODO
    title: str
    author: str
    genre: str = None


class User(BaseModel): #TODO
    login: str
    first_name: str
    last_name: str
    #hash: str надо подумать


class Ratings(BaseModel): #TODO
    """оценка трека, текущий юзер"""
    #hash: str
    track_id: int
    estimate: int

class DeleteTrack(BaseModel):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str
