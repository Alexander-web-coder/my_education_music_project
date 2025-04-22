from fastapi import FastAPI
from app.routes import track, users

app = FastAPI(
    title="Трекер музыкальных предпочтений",
    description="Учебный проект для сбора статистики музыкальных предпочтений на"
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
