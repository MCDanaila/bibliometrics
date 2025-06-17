from typing import Dict
from typing import List
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlmodel import Field
from sqlmodel import JSON
from sqlmodel import Relationship
from sqlmodel import SQLModel

__all__ = ("ScopusSource",)


class ScopusSource(SQLModel, table=True):

    __tablename__ = "ScopusSource"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), primary_key=True),
    )
    name: str = Field(index=True)
    abbrev: Optional[str]
    issn: Optional[List[str]]
    codencode: Optional[str]
    publisher: Optional[str]

    publications: List["ScopusPublication"] = Relationship(
        back_populates="source"
    )
