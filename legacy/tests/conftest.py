import pytest
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import SQLModel

POSTGRES_USER = "ethz_biblio"
POSTGRES_PASSWORD = "password"
POSTGRES_SERVER = "localhost"
POSTGRES_PORT = "5433"
POSTGRES_DB = "testbiblio"

POSTGRES_TEST_URI = "postgresql://"
POSTGRES_TEST_URI += f"{POSTGRES_USER}"
POSTGRES_TEST_URI += f":{POSTGRES_PASSWORD}"
POSTGRES_TEST_URI += f"@{POSTGRES_SERVER}"
POSTGRES_TEST_URI += f":{POSTGRES_PORT}"
POSTGRES_TEST_URI += f"/{POSTGRES_DB}"


@pytest.fixture(scope="function")
def db():
    engine = create_engine(POSTGRES_TEST_URI, echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()
    SQLModel.metadata.drop_all(engine)
