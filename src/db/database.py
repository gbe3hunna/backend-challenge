import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)

POSTGRES_DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
                         f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(POSTGRES_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_fastapi():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_celery():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
