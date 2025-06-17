from typing import List
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

__all__ = (
    "ScopusAuthorship",
    "ScopusAffiliation",
    "ScopusAuthor",
)


class ScopusAuthor(SQLModel, table=True):

    __tablename__ = "ScopusAuthor"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), primary_key=True),
    )
    degrees: Optional[str]
    given_name: Optional[str]
    surname: Optional[str]
    indexed_name: Optional[str]
    preferred_name: Optional[str]
    e_address: Optional[str]

    authorships: List["ScopusAuthorship"] = Relationship(
        back_populates="author"
    )

    @property
    def publications(self):
        return (x.publication for x in self.authorships)

    @property
    def affiliations(self):
        return (x.affiliation for x in self.authorships)


class ScopusAffiliation(SQLModel, table=True):

    __tablename__ = "ScopusAffiliation"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger(), primary_key=True),
    )

    afid: Optional[int] = Field(
        default=None,
        index=True,
        sa_column=Column(BigInteger()),
    )

    dptid: Optional[int] = Field(
        default=None,
        index=True,
        sa_column=Column(BigInteger()),
    )
    organization: Optional[str] = Field(index=True)

    country: Optional[str]
    address: Optional[str]
    city: Optional[str]

    authorships: List["ScopusAuthorship"] = Relationship(
        back_populates="affiliation"
    )

    @property
    def publications(self):
        return (x.publication for x in self.authorships)

    @property
    def authors(self):
        return (x.author for x in self.authorships)


class ScopusAuthorship(SQLModel, table=True):

    __tablename__ = "ScopusAuthorship"

    publication_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            BigInteger(),
            ForeignKey("ScopusPublication.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )
    publication: "ScopusPublication" = Relationship(
        back_populates="authorships"
    )

    author_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            BigInteger(),
            ForeignKey("ScopusAuthor.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )
    author: "ScopusAuthor" = Relationship(back_populates="authorships")

    affiliation_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            BigInteger(),
            ForeignKey("ScopusAffiliation.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )
    affiliation: "ScopusAffiliation" = Relationship(
        back_populates="authorships"
    )

    seq: Optional[int]
