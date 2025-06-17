def parse_source(source) -> ScopusSource:
    try:
        conference_info_data = source.additional_srcinfo.conferenceinfo
    except AttributeError:
        conference_info_data = False
        conference_info = None
    if (
        conference_info_data
        and conference_info_data.confevent
        and conference_info_data.confevent.confcode
    ):
        confevent = conference_info_data.confevent
        confpublication = conference_info_data.confpublication
        try:
            conflocation = confevent.conflocation
            conflocation_dict = dict(
                country=conflocation.country,
                city=conflocation.city or conflocation.city_group,
                # postal_code=conflocation.postal_code or None,
            )
        except AttributeError:
            conflocation_dict = {}
        try:
            confdate = confevent.confdate
            dates_dict = dict(
                start_date=date(
                    int(confdate.startdate.year),
                    int(confdate.startdate.month),
                    int(confdate.startdate.day),
                ),
                end_date=date(
                    int(confdate.enddate.year),
                    int(confdate.enddate.month),
                    int(confdate.enddate.day),
                ),
            )
        except AttributeError:
            dates_dict = {}
        conference_info = ScopusConferenceInfoJSON(
            id=re.sub("[^0-9]", "", confevent.confcode),
            name=confevent.confname.content[0],
            IEEE_catnumber=confevent.confcatnumber,
            edition=None,  # TODO find example
            sponsors=get_attribute(confevent, "confsponsors", "confsponsor"),
            editors=[
                ScopusConferenceEditorJSON(
                    name_or_initials=editor.given_name
                    or editor.initials
                    or editor.indexed_name,
                    surname=editor.surname,
                )
                for editor in get_attribute(
                    confpublication,
                    "confeditors",
                    "editors",
                    "editor",
                    default=(),
                )
            ],
            **conflocation_dict,
            **dates_dict,
        )
    else:
        conference_info = None
    if source.sourcetitle:
        _name = source.sourcetitle.content[0]
    else:
        _name = None
    return ScopusSource(
        id=source.srcid,
        name=_name,
        abbrev=abbrev,
        issn=[n.content[0] for n in source.issn if source.issn],
        codencode=source.codencode,
        publisher=", ".join(
            [
                p.publishername
                for p in source.publisher
                if isinstance(p.publishername, str)
            ]
        ),
        conference_info=conference_info,
    )


def parse_bibliography(
    bibrecords: TailTp, pub_scpid: Tuple[int]
) -> List[ScopusCitation]:
    """Auxiliary function for 'read_publication'.

    Args:
        bibrecord:
            xml element containing information about
            the bibliography of the publication.
        pub_scpid:
            tuple containg just the id of the current pubblication
            (a.k.a the citing publication).

    Returns:
        cit:
            a flat list of WoSCitations.
    """

    if bibrecords is None:
        return []
    bibliography = bibrecords.bibliography
    refs = bibliography.reference
    sgrids = [
        r.ref_info.refd_itemidlist.itemid[0].content[0]
        for r in refs
        if r.ref_info.refd_itemidlist.itemid[0].idtype == "SGR"
    ]
    bibliography = [
        ScopusCitation(citing_id=pub_scpid, cited_id=sgrid) for sgrid in sgrids
    ]
    return bibliography

    # refcount = get(bibliography, ["@refcount"])
    #### str

    # reference = get(bibliography, ["reference"])  # list
    #### [['@id', 'ref-info', 'ref-fulltext']] == [[str, {}, str]]

    # ref_info = get(reference[0], ["ref-info"])  # EXAMPLE with index 0
    ###### ['ref-title', 'refd-itemidlist', 'ref-authors', 'ref-sourcetitle', 'ref-publicationyear', 'ref-volisspag']
    #
    # ref_title = get(ref_info, ["ref-title"])
    ####### ['ref-titletext']
    #
    # ref_titletext = get(ref_title, ["ref-titletext"])
    ######## str
    #
    # refd_itemidlist = get(ref_info, ["refd-itemidlist"])
    ####### ['itemid']
    #
    # itemid2 = get(refd_itemidlist, ["itemid"])
    ######## ['@idtype', '#text']
    #
    # itemid2_idtype = get(itemid2, ["@idtype"])
    ######### str
    #
    # itemid2_text = get(itemid2, ["#text"])
    ######### str
    #
    # ref_authors = get(ref_info, ["ref-authors"])
    ####### ['author']
    #
    # ref_authors_author = get(ref_authors, ["author"])  # list
    ######## [['@seq', 'ce:initials', 'ce:indexed-name', 'ce:surname']] == [[str, str, str, str]]
    #
    # ref_sourcetitle = get(ref_info, ["ref-sourcetitle"])
    ####### str
    #
    # ref_publicationyear = get(ref_info, ["ref-publicationyear"])
    ####### ['@first'] == [str]
    #
    # ref_volisspag = get(ref_info, ["ref-volisspag"])
    ####### ['@volume', 'pagerange'] == [str, {}]
    #
    # pagerange = get(ref_volisspag, ["pagerange"])
    ######## ['@first'] == str
