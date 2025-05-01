"""Главный модуль"""
from fastapi import FastAPI
from app.routers import tracks, users, ratings
from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, InternalError, IntegrityError

from contextlib import asynccontextmanager
from .db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Асинхронный генератор"""
    init_database()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Сервис музыкальных рекомендаций",
    description="Учебный проект для сбора статистики музыкальных предпочтений на "
                "фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Александр",
        "url": "https://fake.url",
        "email": "sample@sample.url",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"Информация":"перейдите на http://127.0.0.1:8000/docs"}


app.include_router(tracks.router)
app.include_router(users.router)
app.include_router(ratings.router)
