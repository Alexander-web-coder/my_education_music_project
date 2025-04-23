from pydantic import BaseModel

class Track(BaseModel): #TODO
    title: str
    author: str
    genre: list[str] = None


class User(BaseModel): #TODO
    login: str
    first_name: str
    last_name: str
    #hash: str надо подумать


class ratings(Track, User): #TODO
    """отправляет название и автора трека, оценку и логин"""
    estimate: int
