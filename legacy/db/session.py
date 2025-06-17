from devtools import debug
from sqlmodel import create_engine
from sqlmodel import Session

from libbiblio.db.config import settings

SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # echo=True,
)


def get_db():
    db = Session(engine, autoflush=False)
    try:
        yield db
    finally:
        db.rollback()
        db.close()
