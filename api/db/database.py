import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
SQLITE_DB_URL = f"sqlite:///{ROOT_PATH}/db/db.sqlite"

engine = create_engine(SQLITE_DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()