"""Главный модуль"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import tracks, users, ratings
from .db import init_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Асинхронный контекст-менеджер"""
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

templates = Jinja2Templates(directory="app/templates")

@app.get("/", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def root(request: Request):
    """Вывод страницы с приветствием"""
    return templates.TemplateResponse(request, "index.html")

# @app.get("/", status_code=status.HTTP_200_OK, tags=["Главная страница"])
# def root() -> dict:
#     """Заглавная страница"""
#     return {"Для информации":"перейдите на http://127.0.0.1:80/docs"}


app.include_router(tracks.router)
app.include_router(users.router)
app.include_router(ratings.router)
