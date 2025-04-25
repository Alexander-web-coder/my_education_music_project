from fastapi import FastAPI
from app.routers import track, users, ratings

from contextlib import asynccontextmanager  # Uncomment if you need to create tables on app start >>>
from app.db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
   init_database()
   yield


app = FastAPI(
    lifespan=lifespan,
    title="Трекер музыкальных предпочтений",
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

# @app.get("/")
# def root():
#     return {"Заглушка":"Новый проект"}

app.include_router(track.router)
app.include_router(users.router)
app.include_router(ratings.router)
