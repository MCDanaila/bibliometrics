from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

from devtools import debug  # noqa

from ...db.models.web_of_science import NotLinkedWoSCitation
from ...db.models.web_of_science import WoSAffiliation
from ...db.models.web_of_science import WoSAuthor
from ...db.models.web_of_science import WoSAuthorship
from ...db.models.web_of_science import WoSCitation  # type:ignore
from ...db.models.web_of_science import WoSGrant
from ...db.models.web_of_science import WoSPublication  # type:ignore
from ...db.models.web_of_science import WoSSource


class WoSParserError(Exception):
    pass


def get(data, keys):
    element = data
    for key in keys:
        if isinstance(element, dict) and (key in element):
            element = element[key]
        else:
            return None
    return element


def get_id(data) -> int:
    ret = get(data, ["UID"])
    return ret


def get_doi(data):
    identifier_list = get(
        data,
        [
            "dynamic_data",
            "cluster_related",
            "identifiers",
            "identifier",
        ],
    )
    for identifier in identifier_list:
        if get(identifier, ["@type"]) == "xref_doi":
            return get(identifier, ["@value"])


def get_accession_no(data):
    identifier_list = get(
        data,
        [
            "dynamic_data",
            "cluster_related",
            "identifiers",
            "identifier",
        ],
    )
    for identifier in identifier_list:
        if get(identifier, ["@type"]) == "accession_no":
            return get(identifier, ["@value"])


def get_pmid(data):
    identifier_list = get(
        data,
        [
            "dynamic_data",
            "cluster_related",
            "identifiers",
            "identifier",
        ],
    )
    for identifier in identifier_list:
        if get(identifier, ["@type"]) == "pmid":
            return get(identifier, ["@value"])


def get_pub_type(data):
    pub_type = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "normalized_doctypes",
            "doctype",
        ],
    )
    if isinstance(pub_type, str):
        return [pub_type]
    else:
        return pub_type


def get_pub_lan(data):
    language = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "languages",
        ],
    )
    if get(language, ["@count"]) == "1":
        return get(language, ["language", "#text"])
    else:
        languages = get(language, ["language"])
        return " - ".join([get(lang, ["#text"]) for lang in languages])


def get_title(data):
    titles = get(data, ["static_data", "summary", "titles", "title"])
    for title in titles:
        if title["@type"] == "item":
            return title["#text"]


def get_author_keywords(data):
    return get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "keywords",
            "keyword",
        ],
    )


def get_page_first(data):
    return get(data, ["static_data", "summary", "pub_info", "page", "@begin"])


def get_page_last(data):
    return get(data, ["static_data", "summary", "pub_info", "page", "@end"])


def get_publication_year(data):
    return get(data, ["static_data", "summary", "pub_info", "@pubyear"])


def get_publication_month(data):
    return get(data, ["static_data", "summary", "pub_info", "@month"])


def get_publication_date(data):
    return get(data, ["static_data", "summary", "pub_info", "@sortdate"])


def get_volume(data):
    return get(data, ["static_data", "summary", "pub_info", "@vol"])


def get_copyright(data):
    return get(data, ["@r_id_disclaimer"])


def get_wuid(data):
    edition = get(data, ["static_data", "summary", "EWUID", "edition"])
    ret = []
    if edition:
        if isinstance(edition, dict):
            edition = [edition]
        for wuid in edition:
            ret.append(get(wuid, ["@value"]))
    return ret


def get_headings(data):
    headings = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "category_info",
            "headings",
            "heading",
        ],
    )
    if headings:
        if isinstance(headings, str):
            headings = [headings]
        return headings
    else:
        return []


def get_subheadings(data):
    subheadings = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "category_info",
            "subheadings",
            "subheading",
        ],
    )
    if subheadings:
        if isinstance(subheadings, str):
            subheadings = [subheadings]
        return subheadings
    else:
        return []


def get_subjects(data):
    subjects = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "category_info",
            "subjects",
            "subject",
        ],
    )
    ret = []
    if subjects:
        for subject in subjects:
            ret.append(get(subject, ["#text"]))
    return ret


def get_abstract(data):
    abstract = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "abstracts",
            "abstract",
            "abstract_text",
            "p",
        ],
    )
    return abstract[0] if isinstance(abstract, list) else abstract


def get_fund_text(data):
    return get(
        data,
        ["static_data", "fullrecord_metadata", "fund_ack", "fund_text", "p"],
    )


def get_source(db, data):
    title_ = get(data, ["static_data", "summary", "titles", "title"])
    title = {ttl["@type"]: ttl["#text"] for ttl in title_}
    name = get(title, ["source"])
    if name:
        name = name.capitalize()
        query_source = (
            db.query(WoSSource).where(WoSSource.name == name).first()
        )
        if query_source:
            return query_source
        else:

            publisher = get(
                data,
                [
                    "static_data",
                    "summary",
                    "publishers",
                    "publisher",
                    "name",
                    "unified_name",
                ],
            )
            identifier_list = get(
                data,
                [
                    "dynamic_data",
                    "cluster_related",
                    "identifiers",
                    "identifier",
                ],
            )
            issn = None
            for identifier in identifier_list:
                if get(identifier, ["@type"]) == "issn":
                    issn = get(identifier, ["@value"])
                    break

            return WoSSource(
                name=name,
                abbrev_iso=get(title, ["abbrev_iso"]),
                source_abbrev=get(title, ["source_abbrev"]),
                abbrev_11=get(title, ["abbrev_11"]),
                abbrev_29=get(title, ["abbrev_29"]),
                publisher=publisher,
                issn=issn,
            )


def get_affiliations_dict(db, addresses: Dict) -> Dict[str, WoSAffiliation]:

    affiliations_dict = {}
    for affiliation in addresses:

        addr_no = get(affiliation, ["@addr_no"])
        if addr_no:
            organizations_list = []
            organizations = get(affiliation, ["organizations", "organization"])
            if organizations:
                if isinstance(organizations, str):
                    organizations_list.append(organizations)
                else:
                    for org in organizations:
                        if isinstance(org, dict):
                            organizations_list.append(get(org, ["#text"]))
                        else:
                            organizations_list.append(org)
            suborganizations = get(
                affiliation, ["suborganizations", "suborganization"]
            )
            if suborganizations:
                if isinstance(suborganizations, str):
                    organizations_list.append(suborganizations)
                else:
                    for suborg in suborganizations:
                        organizations_list.append(suborg)

            if not organizations_list:  # RARE
                organizations_list = [
                    get(affiliation, ["full_address"]) or "NOT FOUND"
                ]

            full_address = get(affiliation, ["full_address"])
            country = get(affiliation, ["country"])
            state = get(affiliation, ["state"])
            city = get(affiliation, ["city"])
            street = get(affiliation, ["street"])
            postal_code = get(affiliation, ["zip"])
            if isinstance(postal_code, list):
                postal_code = get(postal_code[0], ["#text"])
            else:
                postal_code = get(postal_code, ["#text"])

            query_affiliation = (
                db.query(WoSAffiliation)
                .where(WoSAffiliation.organization == organizations_list[0])
                .first()
            )

            if query_affiliation:
                affiliations_dict[addr_no] = query_affiliation
            else:
                affiliations_dict[addr_no] = WoSAffiliation(
                    organization=organizations_list[0],
                    sub_organizations=organizations_list[1:],
                    address=full_address,
                    country=country,
                    state=state,
                    city=city,
                    street=street,
                    postal_code=postal_code,
                )

    affiliation0 = db.get(WoSAffiliation, 0)
    if affiliation0:
        affiliations_dict["0"] = affiliation0
    else:
        affiliations_dict["0"] = WoSAffiliation(id=0, organization="null")
    return affiliations_dict


def get_authors_dict(
    db, authors: Dict
) -> Dict[WoSAuthor, List[Tuple[str, str, str]]]:

    authors_dict = {}
    for author in authors:
        addr_no = get(author, ["@addr_no"])
        if not addr_no:
            addr_no = "0"
        seq_no = get(author, ["@seq_no"])
        if not seq_no:
            seq_no = "0"
        role = get(author, ["@role"])
        # reprint = get(author, ['@reprint'])
        orcid_id_tr = get(author, ["@orcid_id_tr"])
        r_id = get(author, ["@r_id"])
        display_name = get(author, ["display_name"])
        full_name = get(author, ["full_name"])
        wos_standard = get(author, ["wos_standard"])
        first_name = get(author, ["first_name"])
        last_name = get(author, ["last_name"])
        email_addr = get(author, ["email_addr"])

        already_in = False
        for author in authors_dict:
            if author.wos_standard == wos_standard:
                for key in addr_no.split():
                    authors_dict[author].append((key, seq_no, role))
                already_in = True
                break
        if not already_in:
            query_author = (
                db.query(WoSAuthor)
                .where(WoSAuthor.wos_standard == wos_standard)
                .first()
            )
            if query_author:
                new = query_author
            else:
                new = WoSAuthor(
                    name=full_name,
                    given_name=first_name,
                    surname=last_name,
                    display_name=display_name,
                    wos_standard=wos_standard,
                    e_address=email_addr,
                    orcid_id=orcid_id_tr,
                    r_id=r_id,
                )

            authors_dict[new] = []
            for key in addr_no.split():
                authors_dict[new].append((key, seq_no, role))
    return authors_dict


def make_authorships(
    pub_id: int, affiliations: Dict, authors: Dict
) -> Set[WoSAuthorship]:
    authorships_list = []
    for author, ksr_list in authors.items():
        for ksr in ksr_list:
            already_in = False
            for authorship in authorships_list:
                if (
                    authorship.publication_id == pub_id
                    and authorship.affiliation == affiliations[ksr[0]]
                    and authorship.author == author
                ):
                    already_in = True
                    break
            if not already_in:
                authorships_list.append(
                    WoSAuthorship(
                        publication_id=pub_id,
                        affiliation=affiliations[ksr[0]],
                        author=author,
                        seq=ksr[1],
                        role=ksr[2],
                    )
                )
    new_authorships_list = list(set(authorships_list))
    return new_authorships_list


def get_authorships(db, data: Dict) -> List[WoSAuthorship]:
    addresses = get(data, ["static_data", "fullrecord_metadata", "addresses"])

    # affiliations_dict
    count = get(addresses, ["@count"])
    address_specs = []
    if count and (count != "0"):
        address_name = get(addresses, ["address_name"])
        if isinstance(address_name, dict):
            address_specs.append(get(address_name, ["address_spec"]))
        elif isinstance(address_name, list):
            for address in address_name:
                address_specs.append(get(address, ["address_spec"]))

    affiliations_dict = get_affiliations_dict(db, address_specs)

    # authors_dict
    name = get(addresses, ["address_name", "names", "name"])
    names = []
    if name:
        if isinstance(name, dict):
            names.append(name)
        elif isinstance(name, list):
            for n in name:
                names.append(n)

    contributor = get(data, ["static_data", "contributors", "contributor"])
    contributors = []
    if contributor:
        if isinstance(contributor, dict):
            contributors.append(contributor["name"])
        elif isinstance(contributor, list):
            for c in contributor:
                contributors.append(c["name"])
    summary = get(data, ["static_data", "summary", "names", "name"])
    summary_names = []
    if summary:
        if isinstance(summary, dict):
            summary_names.append(summary)
        elif isinstance(summary, list):
            for s in summary:
                summary_names.append(s)

    authors = []
    if names:
        authors = names
    elif summary_names:
        authors = summary_names
    elif contributors:
        authors = contributors

    authors_dict = get_authors_dict(db, authors)
    # NOTE: case `authors_dict == {}` is deliberately ignored
    # because it has never been found
    # (could be the cause of future errors)

    # authorships_list
    pub_id = get_id(data)
    authorships_list = make_authorships(
        pub_id=pub_id, affiliations=affiliations_dict, authors=authors_dict
    )

    return authorships_list


def get_grant(data):
    _grant = get(
        data,
        ["static_data", "fullrecord_metadata", "fund_ack", "grants", "grant"],
    )
    if _grant:
        if isinstance(_grant, dict):
            _grant = [_grant]
        g_agency = []
        g_ids = []
        for g in _grant:
            if "grant_agency" in g:
                grant_agency = g.get("grant_agency")
                if isinstance(grant_agency, str):
                    g_agency.append(grant_agency)
                elif isinstance(grant_agency, list):
                    for agency in grant_agency:
                        if isinstance(agency, str):
                            g_agency.append(agency)
                        elif isinstance(agency, dict):
                            if "#text" in agency:
                                g_agency.append(agency.get("#text"))

            grant_id = get(g, ["grant_ids", "grant_id"])
            if grant_id:
                if isinstance(grant_id, str):
                    g_ids.append(grant_id)
                elif isinstance(grant_id, str):
                    for x in grant_id:
                        g_ids.append(x)
        grant = WoSGrant(
            grant_agency=g_agency, grant_ids=g_ids, publication_id=get_id(data)
        )
        return grant


def get_citations(data):
    citations = []
    citing_id = get_id(data)
    references = get(
        data,
        [
            "static_data",
            "fullrecord_metadata",
            "references",
            "reference",
        ],
    )
    if not references:
        return []
    for ref in references:
        # heuristic
        cited_id = get(ref, ["uid"])
        if cited_id:
            _id = cited_id
            if _id.startswith("WOS:"):
                _id = _id[4:]
            _id = max(_id.split("."), key=len)
            if _id.isdigit():
                citations.append(
                    NotLinkedWoSCitation(
                        citing_id=citing_id, cited_id=int(_id)
                    )
                )
            else:
                citations.append(
                    NotLinkedWoSCitation(
                        citing_id=citing_id,
                        cited_id=0,
                        uid=cited_id,
                    )
                )

    return list(set(citations))


def wos_parser(
    db,
    data: Dict,
) -> Tuple[WoSPublication, List[WoSCitation]]:
    pub_id = get_id(data)

    if (not pub_id) or db.get(WoSPublication, pub_id):
        return None, None

    publication = WoSPublication(
        id=pub_id,
        doi=get_doi(data),
        publication_type=get_pub_type(data),
        publication_language=get_pub_lan(data),
        title=get_title(data),
        author_keywords=get_author_keywords(data),
        page_first=get_page_first(data),
        page_last=get_page_last(data),
        publication_year=get_publication_year(data),
        publication_month=get_publication_month(data),
        publication_date=get_publication_date(data),
        volume=get_volume(data),
        copyright=get_copyright(data),
        wuid=get_wuid(data),
        headings=get_headings(data),
        subheadings=get_subheadings(data),
        subjects=get_subjects(data),
        abstract=get_abstract(data),
        fund_text=get_fund_text(data),
        grant=get_grant(data),
        source=get_source(db, data),
        authorships=get_authorships(db, data),
    )
    notlinked_citations = get_citations(data)

    return publication, notlinked_citations
