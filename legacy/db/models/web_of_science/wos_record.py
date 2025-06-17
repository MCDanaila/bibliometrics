from datetime import date
from typing import List
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

__all__ = ("WoSPublication", "WoSCitation", "NotLinkedWoSCitation", "WoSGrant")


class WoSPublication(SQLModel, table=True):

    __tablename__ = "WoSPublication"

    # `id` is not Optional because it's taken from the data
    id: str = Field(primary_key=True)
    doi: Optional[str] = Field(default=None, index=True)

    publication_type: Optional[List[str]]

    publication_language: Optional[str]
    title: str

    author_keywords: Optional[List[str]]

    page_first: Optional[int]
    page_last: Optional[int]
    publication_date: Optional[date]
    publication_year: Optional[int]
    publication_month: Optional[str]
    volume: Optional[str]
    copyright: Optional[str]
    wuid: Optional[List[str]]

    # Category Info
    headings: Optional[List[str]]
    subheadings: Optional[List[str]]
    subjects: Optional[List[str]]

    abstract: Optional[str]

    source_id: Optional[int] = Field(default=None, foreign_key="WoSSource.id")
    source: Optional["WoSSource"] = Relationship(back_populates="publications")

    authorships: List["WoSAuthorship"] = Relationship(
        back_populates="publication"
    )

    @property
    def authors(self):
        return (x.author for x in self.authorships)

    @property
    def affiliations(self):
        return (x.affiliation for x in self.authorships)

    # Funding info
    fund_text: Optional[str]

    grant_id: Optional[int] = Field(default=None, foreign_key="WoSGrant.id")
    grant: Optional["WoSGrant"] = Relationship(back_populates="publication")

    # Bibliography

    bibliography__: List["WoSCitation"] = Relationship(
        back_populates="citing",
        sa_relationship_kwargs={"foreign_keys": "WoSCitation.citing_id"},
    )

    @property
    def bibliography(self):
        return (x.cited for x in self.bibliography__)

    # Incoming citations

    cited_by__: List["WoSCitation"] = Relationship(
        back_populates="cited",
        sa_relationship_kwargs={"foreign_keys": "WoSCitation.cited_id"},
    )

    @property
    def cited_by(self):
        return (x.citing for x in self.cited_by__)


class WoSCitation(SQLModel, table=True):

    __tablename__ = "WoSCitation"
    citing_id: str = Field(foreign_key="WoSPublication.id", primary_key=True)
    citing: WoSPublication = Relationship(
        back_populates="bibliography__",
        sa_relationship_kwargs={"foreign_keys": "WoSCitation.citing_id"},
    )

    cited_id: str = Field(foreign_key="WoSPublication.id", primary_key=True)
    cited: WoSPublication = Relationship(
        back_populates="cited_by__",
        sa_relationship_kwargs={"foreign_keys": "WoSCitation.cited_id"},
    )


class NotLinkedWoSCitation(SQLModel, table=True):

    __tablename__ = "NotLinkedWoSCitation"

    citing_id: str = Field(primary_key=True)
    cited_id: str = Field(primary_key=True)

    uid: Optional[str] = Field(default="", primary_key=True)

    # we define `__hash__` in order to use `set`
    def __hash__(self):
        return hash((self.citing_id, self.cited_id, self.uid))


class WoSGrant(SQLModel, table=True):

    __tablename__ = "WoSGrant"

    id: Optional[int] = Field(default=None, primary_key=True)

    grant_agency: Optional[List[str]]
    grant_ids: Optional[List[str]]

    publication: Optional[WoSPublication] = Relationship(
        back_populates="grant"
    )
