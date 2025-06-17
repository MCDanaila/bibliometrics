from typing import Optional
from typing import Union

from psycopg2 import errors
from psycopg2._psycopg import DatabaseError
from psycopg2._psycopg import DataError
from psycopg2._psycopg import IntegrityError
from psycopg2._psycopg import InterfaceError
from psycopg2._psycopg import InternalError
from psycopg2._psycopg import NotSupportedError
from psycopg2._psycopg import OperationalError
from psycopg2._psycopg import ProgrammingError

from libbiblio.db.models import IngestionLog
from libbiblio.db.session import get_db

__all__ = ("DB_Errors", "error_to_db")

# This is a list of all the errors I got while testing
UniqueViolation = errors.lookup("23505")
DB_Errors = (
    UniqueViolation,
    DatabaseError,
    DataError,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Exception,
)


def error_to_db(
    error,
    *,
    source: str,
    record_id: Optional[Union[int, str]] = None,
    dir_path: Optional[str] = "",
    zip_name: Optional[str] = "",
    xml_name: Optional[str] = "",
):
    db = next(get_db())
    log = IngestionLog(
        source=source,
        record_id=record_id,
        args=str(error),
        dir_path=dir_path,
        zip_name=zip_name,
        xml_name=xml_name,
    )
    db.add(log)
    db.commit()
