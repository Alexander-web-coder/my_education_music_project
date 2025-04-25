from sqlmodel import create_engine, Session

DB_URL = "postgresql://fastapi_music:fastapi_music@127.0.0.1:5432/music_project"

engine = create_engine(DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


