from typing import Dict
from typing import List
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field
from sqlmodel import JSON
from sqlmodel import Relationship
from sqlmodel import SQLModel

__all__ = ("NotLinkedScopusCitation", "ScopusPublication", "ScopusCitation")


class ScopusPublication(SQLModel, table=True):

    __tablename__ = "ScopusPublication"

    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), primary_key=True),
    )
    sgrid: Optional[int] = Field(
        default=None, unique=True, index=True, sa_column=Column(BigInteger())
    )
    doi: Optional[str]
    ce_ern: Optional[str]
    publication_type: Optional[str]
    publication_language: Optional[str]
    title: str
    alt_titles: Optional[List[str]]
    publication_year: Optional[int]
    publication_month: Optional[int]
    publication_day: Optional[int]
    author_keywords: Optional[List[str]]
    volume: Optional[str]
    issue: Optional[str]
    page_first: Optional[int]
    page_last: Optional[int]
    copyright: Optional[str]
    abstract: Optional[str]

    # date_delivered: datetime # ? not in previous ingestor
    # date_sort: date # ? not in previous ingestor
    # status_type: str # ? not in previous ingestor
    # status_state: str # ? not in previous ingestor
    # publisher_article_number: str # ? not in previous ingestor
    # bib_text: str # ? not in previous ingestor
    # classifications # !
    # descriptors # !

    source_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            BigInteger(), ForeignKey("ScopusSource.id", ondelete="SET NULL")
        ),
    )
    source: Optional["ScopusSource"] = Relationship(
        back_populates="publications"
    )
    # extra_source: Optional[str]

    authorships: List["ScopusAuthorship"] = Relationship(
        back_populates="publication"
    )

    extra_authors: Optional[str]
    extra_affiliations: Optional[str]

    @property
    def authors(self):
        return (x.author for x in self.authorships)

    @property
    def affiliations(self):
        return (x.affiliation for x in self.authorships)

    # Bibliography

    bibliography__: List["ScopusCitation"] = Relationship(
        back_populates="citing",
        sa_relationship_kwargs={"foreign_keys": "ScopusCitation.citing_id"},
    )

    @property
    def bibliography(self):
        return (x.cited for x in self.bibliography__)

    # Incoming citations

    cited_by__: List["ScopusCitation"] = Relationship(
        back_populates="cited",
        sa_relationship_kwargs={"foreign_keys": "ScopusCitation.cited_id"},
    )

    @property
    def cited_by(self):
        return (x.citing for x in self.cited_by__)


class ScopusCitation(SQLModel, table=True):

    __tablename__ = "ScopusCitation"

    citing_id: int = Field(
        sa_column=Column(
            BigInteger(),
            ForeignKey("ScopusPublication.id"),
            primary_key=True,
        ),
    )
    citing: "ScopusPublication" = Relationship(
        back_populates="bibliography__",
        sa_relationship_kwargs={"foreign_keys": "ScopusCitation.citing_id"},
    )
    cited_id: int = Field(
        sa_column=Column(
            BigInteger(),
            ForeignKey("ScopusPublication.id"),
            primary_key=True,
        ),
    )
    cited: "ScopusPublication" = Relationship(
        back_populates="cited_by__",
        sa_relationship_kwargs={"foreign_keys": "ScopusCitation.cited_id"},
    )


class NotLinkedScopusCitation(SQLModel, table=True):

    __tablename__ = "NotLinkedScopusCitation"

    citing_id: int = Field(sa_column=Column(BigInteger(), primary_key=True))
    cited_sgrid: int = Field(sa_column=Column(BigInteger(), primary_key=True))

    # we define `__hash__` in order to use `set`
    def __hash__(self):
        return hash((self.citing_id, self.cited_sgrid))
