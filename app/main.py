from fastapi import FastAPI
from app.routers import track, users, ratings
from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, InternalError, IntegrityError

from contextlib import asynccontextmanager  # Uncomment if you need to create tables on app start >>>
from app.db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
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

@app.get("/")
def root():
    return {"Информация":"перейдите на http://127.0.0.1:8000/docs"}

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    # Для ошибок целостности (например, дублирование уникального ключа)
    return JSONResponse(
            status_code=400,
            content={"message": "Нарушены ограничения базы данных. Запись не уникальна либо не существует."},
        )

app.include_router(track.router)
app.include_router(users.router)
app.include_router(ratings.router)
