from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Entities.base import Base  # jediný Base, který používají všechny entity

DATABASE_URL = "sqlite:///./databaze.sqlite"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
