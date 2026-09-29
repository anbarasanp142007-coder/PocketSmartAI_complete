from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from .config import get_settings

s=get_settings()
engine=create_engine(s.database_url, connect_args={"check_same_thread":False} if s.database_url.startswith("sqlite") else {})
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase): pass

def get_db() -> Generator[Session,None,None]:
    db=SessionLocal()
    try: yield db
    finally: db.close()

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
