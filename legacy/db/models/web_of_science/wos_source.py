from typing import List
from typing import Optional

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

__all__ = ("WoSSource",)


class WoSSource(SQLModel, table=True):

    __tablename__ = "WoSSource"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    issn: Optional[str] = Field(default=None, index=True)
    abbrev: Optional[str]
    publisher: Optional[str]
    source_abbrev: Optional[str]
    abbrev_iso: Optional[str]
    abbrev_11: Optional[str]
    abbrev_29: Optional[str]

    publications: List["WoSPublication"] = Relationship(
        back_populates="source"
    )
