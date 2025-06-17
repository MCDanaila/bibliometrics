from datetime import datetime
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


__all__ = ("IngestionLog",)


class IngestionLog(SQLModel, table=True):

    __tablename__ = "IngestionLog"

    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    record_id: str = Field(default="")
    args: str
    timestamp: datetime = Field(default=datetime.utcnow())

    dir_path: Optional[str] = Field(default="")
    zip_name: Optional[str] = Field(default="")
    xml_name: Optional[str] = Field(default="")
