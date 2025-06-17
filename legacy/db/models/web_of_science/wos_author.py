from typing import List
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

__all__ = (
    "WoSAuthor",
    "WoSAffiliation",
    "WoSAuthorship",
)


class WoSAuthor(SQLModel, table=True):

    __tablename__ = "WoSAuthor"

    # id: Optional[int] = Field(default=None, primary_key=True)
    wos_standard: str = Field(primary_key=True)
    name: Optional[str]
    given_name: Optional[str]
    surname: Optional[str]
    name_suffix: Optional[str]
    e_address: Optional[str]
    display_name: Optional[str]
    orcid_id: Optional[str]
    r_id: Optional[str]

    authorships: List["WoSAuthorship"] = Relationship(back_populates="author")

    @property
    def publications(self):
        return (x.publication for x in self.authorships)

    @property
    def affiliations(self):
        return (x.affiliation for x in self.authorships)

    def __hash__(self):
        return hash(self.wos_standard)

    def __eq__(self, other):
        return self.wos_standard == other.wos_standard


class WoSAffiliation(SQLModel, table=True):

    __tablename__ = "WoSAffiliation"

    id: Optional[int] = Field(default=None, primary_key=True)
    organization: str = Field(index=True)
    sub_organizations: Optional[List[str]] = Field(default=[])
    address: Optional[str]
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    street: Optional[str]
    postal_code: Optional[str]

    authorships: List["WoSAuthorship"] = Relationship(
        back_populates="affiliation"
    )

    @property
    def publications(self):
        return (x.publication for x in self.authorships)

    @property
    def authors(self):
        return (x.author for x in self.authorships)

    def __eq__(self, other):
        return self.organization == other.organization


class WoSAuthorship(SQLModel, table=True):

    __tablename__ = "WoSAuthorship"

    publication_id: Optional[str] = Field(
        foreign_key="WoSPublication.id", primary_key=True
    )
    publication: Optional["WoSPublication"] = Relationship(
        back_populates="authorships"
    )

    author_id: str = Field(  # Optional[int] = Field(
        # default=None, foreign_key="wosauthor.id", primary_key=True
        foreign_key="WoSAuthor.wos_standard",
        primary_key=True,
    )
    author: Optional[WoSAuthor] = Relationship(back_populates="authorships")

    affiliation_id: Optional[int] = Field(
        default=None, foreign_key="WoSAffiliation.id", primary_key=True
    )
    affiliation: Optional[WoSAffiliation] = Relationship(
        back_populates="authorships"
    )

    def __repr__(self):
        return str(
            (
                self.publication_id,
                self.author.wos_standard,
                self.affiliation.organization,
            )
        )

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return hash(
            (
                self.publication_id,
                self.author.wos_standard,
                self.affiliation.organization,
            )
        )

    def __eq__(self, other):
        return (
            self.publication_id == other.publication_id
            and self.author.wos_standard == other.author.wos_standard
            and self.affiliation.organization == other.affiliation.organization
        )

    seq: Optional[int]
    role: Optional[str]
