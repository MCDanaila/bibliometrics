import random
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from devtools import debug

from libbiblio.db.models.scopus import NotLinkedScopusCitation
from libbiblio.db.models.scopus import ScopusAffiliation
from libbiblio.db.models.scopus import ScopusAuthor
from libbiblio.db.models.scopus import ScopusAuthorship
from libbiblio.db.models.scopus import ScopusCitation
from libbiblio.db.models.scopus import ScopusPublication
from libbiblio.db.models.scopus import ScopusSource


def get(data, keys):
    element = data
    for key in keys:
        if isinstance(element, dict) and (key in element):
            element = element[key]
        else:
            return None
    return element


def get_id(data: Dict):
    itemid = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "item-info",
            "itemidlist",
            "itemid",
        ],
    )
    for x in itemid:
        if x["@idtype"] == "SCP":
            return x["#text"]
    raise Exception("ID not found")


def get_sgrid(data: Dict):
    itemid = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "item-info",
            "itemidlist",
            "itemid",
        ],
    )
    for x in itemid:
        if x["@idtype"] == "SGR":
            return x["#text"]
    raise Exception("SGRID not found")


def get_doi(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "item-info",
            "itemidlist",
            "ce:doi",
        ],
    )


def get_pii(data: Dict):
    pii = get(data, ["xocs:doc", "xocs:meta", "xocs:pii"])
    pii2 = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "item-info",
            "itemidlist",
            "ce:pii",
        ],
    )
    return pii or pii2


def get_pub_type(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "citation-info",
            "citation-type",
            "@code",
        ],
    )


def get_pub_lan(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "citation-info",
            "citation-language",
            "@xml:lang",
        ],
    )


def get_title(data: Dict):
    titletext = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "citation-title",
            "titletext",
        ],
    )
    if isinstance(titletext, Dict):
        return get(titletext, ["#text"])
    elif isinstance(titletext, List):
        for title in titletext:
            if get(title, ["@original"]) == "y":
                return get(title, ["#text"])
    else:
        raise Exception("TITLE not found")


def get_alt_titles(data: Dict):
    titletext = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "citation-title",
            "titletext",
        ],
    )
    if isinstance(titletext, Dict):
        return None
    elif isinstance(titletext, List):
        alt_titles = []
        already_have_title = False
        for title in titletext:
            if get(title, ["@original"]) == "y" and not already_have_title:
                already_have_title = True
            else:
                alt_titles.append(get(title, ["#text"]))
        return alt_titles
    else:
        raise Exception("TITLE not found")


def get_publication_year(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "source",
            "publicationdate",
            "year",
        ],
    )


def get_publication_month(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "source",
            "publicationdate",
            "month",
        ],
    )


def get_publication_day(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "source",
            "publicationdate",
            "day",
        ],
    )


def get_author_keywords(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "citation-info",
            "author-keywords",
            "author-keyword",
        ],
    )


def get_volume(data: Dict):
    return get(data, ["xocs:doc", "xocs:meta", "xocs:volume"])


def get_issue(data: Dict):
    return get(data, ["xocs:doc", "xocs:meta", "xocs:issue"])


def get_firstpage(data: Dict):
    return get(data, ["xocs:doc", "xocs:meta", "xocs:firstpage"])


def get_lastpage(data: Dict):
    return get(data, ["xocs:doc", "xocs:meta", "xocs:lastpage"])


def get_copyright(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "item-info",
            "copyright",
            "#text",
        ],
    )


def get_abstract(data: Dict):
    return get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "abstracts",
            "abstract",
            "ce:para",
        ],
    )


def get_source(db, data: Dict) -> ScopusSource:
    source = get(
        data, ["xocs:doc", "xocs:item", "item", "bibrecord", "head", "source"]
    )
    id = get(source, ["@srcid"])
    name = get(source, ["sourcetitle"])
    abbrev = get(source, ["sourcetitle-abbrev"])
    _issn = get(source, ["issn"])
    issn = []
    if isinstance(_issn, str):
        issn.append(_issn)
    elif isinstance(_issn, dict):
        issn.append(get(_issn, "#text"))
    elif isinstance(_issn, list):
        issn += [_["#text"] for _ in _issn]
    else:
        issn = None
    codencode = get(source, ["codencode"])
    publisher = get(source, ["publisher"])
    new_source = ScopusSource(
        id=id,
        name=name,
        abbrev=abbrev,
        issn=issn,
        codencode=codencode,
        publisher=publisher,
    )
    return new_source


def afid0(db, affiliations: Dict):
    if 0 not in affiliations:
        affiliation0 = db.get(ScopusAffiliation, 0)
        if affiliation0:
            affiliations[0] = affiliation0
        else:
            affiliations[0] = ScopusAffiliation(id=0)
    return 0


def auid0(db, authors: Dict):
    if 0 not in authors:
        affiliation0 = db.get(ScopusAuthor, 0)
        if affiliation0:
            authors[0] = affiliation0
        else:
            authors[0] = ScopusAuthor(id=0)
    return 0, 0


def make_affiliation(db, group: Dict, affiliations: Dict):
    affiliation = get(group, ["affiliation"])
    if isinstance(affiliation, list):
        affiliation = affiliation[0]
        # NOTE: As far as observed, all these lists appear to have length 1.
        # Therefore, the implementation choice is to simply take the single
        # dictionary in it.
    afid = get(affiliation, ["@afid"]) or random.randint(-99999, -10000)
    afid = int(afid)
    # NOTE: the random negative integer is used to handle the case where `afid`
    # is not present while keep using `afid` as key in `affiliations` dict.
    query_affiliation = (
        db.query(ScopusAffiliation)
        .where(ScopusAffiliation.afid == afid)
        .first()
    )

    if query_affiliation:
        affiliations[afid] = query_affiliation
    else:
        dptid = get(affiliation, ["@dptid"])
        country = get(affiliation, ["@country"])
        organization = get(affiliation, ["organization"])
        if isinstance(organization, str):
            organization = [organization]
        if organization:
            organization = ", ".join(organization)
        address = get(affiliation, ["address-part"])
        city = get(affiliation, ["city-group"])
        if afid < 0:
            afid = None
        affiliations[afid] = ScopusAffiliation(
            afid=afid,
            dptid=dptid,
            country=country,
            organization=organization,
            address=address,
            city=city,
        )
    return afid


def make_author(
    db, group: Dict, authors: Dict
) -> List[Tuple[ScopusAuthor, int]]:
    return_list = []
    _author = get(group, ["author"])
    if isinstance(_author, dict):
        _author = [_author]
        # As far as observed, sometimes `_author` is a dictionary representing
        # a single author, sometimes it is a list of such dictionaries.
        # Therefore the implementation choice is to put the single author
        # in a list, so that the two cases are then treated the same way.
    for author in _author:
        auid = get(author, ["@auid"])
        if not auid:
            return_list.append(auid0(db, authors))
        elif auid in authors:
            seq = get(author, ["@seq"])
            return_list.append((auid, seq))
        else:
            query_author = db.get(ScopusAuthor, auid)
            seq = get(author, ["@seq"])
            if query_author:
                authors[auid] = query_author
            else:
                authors[auid] = ScopusAuthor(
                    id=auid,
                    degrees=get(author, ["ce:degrees"]),
                    surname=get(author, ["ce:surname"]),
                    given_name=get(author, ["ce:given-name"]),
                    indexed_name=get(author, ["ce:indexed-name"]),
                    e_address=get(author, ["ce:e-address", "#text"]),
                )
            return_list.append((auid, seq))
    return return_list


def get_authorships(
    db, data: Dict
) -> Tuple[List[ScopusAuthorship], List[Dict[Any, Any]], List[Dict[Any, Any]]]:
    author_group = get(
        data,
        ["xocs:doc", "xocs:item", "item", "bibrecord", "head", "author-group"],
    )
    if author_group is None:
        return []

    if isinstance(author_group, dict):
        author_group = [author_group]

    affiliations = {}
    authors = {}
    authorships = {}
    for group in author_group:

        if (not group) or isinstance(group, str):
            # almost never occurs
            afid = afid0(db, affiliations)
            authors_list = [auid0(db, authors)]
        elif get(group, ["affiliation"]) and (not get(group, ["author"])):
            # almost never occurs
            afid = make_affiliation(db, group, affiliations)
            authors_list = auid0(db, authors)
        elif (not get(group, ["affiliation"])) and get(group, ["author"]):
            # sometimes occurs
            """
            This is an example of when afid0 is used:

            author_group: [
                {
                    'author': [
                        {
                            ...
                        },
                        ...
                        {
                            ...
                        },
                    ]
                    'affiliation': [
                        {
                            ...
                        },
                    ],
                },
                {
                    'author': [
                        {
                            ...
                        },
                        ...
                        {
                            ...
                        },
                    ]
                },
            ] (list) len=2

            We cannot find an affiliation for the second group of authors.
            Thus we use `afid0`.
            """
            afid = afid0(db, affiliations)
            authors_list = make_author(db, group, authors)
        else:
            # most of the cases
            afid = make_affiliation(db, group, affiliations)
            authors_list = make_author(db, group, authors)

        for author in authors_list:
            auid = author[0]
            seq = author[1]
            k = (afid, auid)
            if k not in authorships:
                authorships[k] = ScopusAuthorship(
                    author=authors[auid],
                    affiliation=affiliations[afid],
                    seq=seq,
                )
    return list(authorships.values())


def get_citations(data: Dict) -> List[NotLinkedScopusCitation]:
    reference = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "tail",
            "bibliography",
            "reference",
        ],
    )
    citing_id = get_id(data)
    bibliography = []

    if reference:
        for ref in reference:
            if (
                get(ref, ["ref-info", "refd-itemidlist", "itemid", "@idtype"])
                == "SGR"
            ):
                cited_sgrid = get(
                    ref, ["ref-info", "refd-itemidlist", "itemid", "#text"]
                )
                bibliography.append(
                    NotLinkedScopusCitation(
                        citing_id=citing_id, cited_sgrid=cited_sgrid
                    )
                )

    return list(set(bibliography))


def scopus_parser(
    db,
    data: Dict,
) -> Tuple[ScopusPublication, List[NotLinkedScopusCitation]]:

    pub_id = get_id(data)

    if (not pub_id) or db.get(ScopusPublication, pub_id):
        return None, None

    source_id = get(
        data,
        [
            "xocs:doc",
            "xocs:item",
            "item",
            "bibrecord",
            "head",
            "source",
            "@srcid",
        ],
    )
    query_source = db.get(ScopusSource, source_id)
    if query_source:
        source = query_source
        extra_source = get_source(db, data).json()
    else:
        source = get_source(db, data)
        extra_source = None

    authorships = get_authorships(db, data)

    publication = ScopusPublication(
        id=pub_id,
        sgrid=get_sgrid(data),
        doi=get_doi(data),
        ce_ern=get_pii(data),
        publication_type=get_pub_type(data),
        publication_language=get_pub_lan(data),
        title=get_title(data),
        alt_titles=get_alt_titles(data),
        publication_year=get_publication_year(data),
        publication_month=get_publication_month(data),
        publication_day=get_publication_day(data),
        author_keywords=get_author_keywords(data),
        volume=get_volume(data),
        issue=get_issue(data),
        page_first=get_firstpage(data),
        page_last=get_lastpage(data),
        copyright=get_copyright(data),
        abstract=get_abstract(data),
        source=source,
        extra_source=extra_source,
        authorships=authorships,
        # enhancement = get(bibrecord, ["head", "enhancement"])
        # ['descriptorgroup', 'classificationgroup'] # TODO
    )

    notlinked_citations = get_citations(data)

    return publication, notlinked_citations
