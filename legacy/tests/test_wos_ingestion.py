import time

import pytest
from devtools import debug  # noqa
from lxml import etree

from libbiblio.db.models.maintenance import IngestionLog
from libbiblio.db.models.web_of_science.wos_author import WoSAuthor
from libbiblio.db.models.web_of_science.wos_author import WoSAuthorship
from libbiblio.db.models.web_of_science.wos_record import WoSPublication
from libbiblio.sources.common.xml_to_dict import xml_to_dict
from libbiblio.sources.web_of_science.wos_ingestor import wos_ingest_dir
from libbiblio.sources.web_of_science.wos_ingestor import wos_ingest_one
from libbiblio.sources.web_of_science.wos_ingestor import wos_treat_zip

# from libbiblio.sources.web_of_science.ingest import wos_ingest_file


@pytest.mark.asyncio
async def test_ingest_one(db_session):
    filename = "tests/test_data/web_of_science/wos_xml_minimal.xml"
    ns = "{http://clarivate.com/schema/wok5.30/public/FullRecord}"
    record_el_iterator = etree.iterparse(filename, tag=f"{ns}REC")
    event, record_el = next(record_el_iterator)
    res = await wos_ingest_one(record_el, "", "")
    debug(res)
    pub = db_session.query(WoSPublication).first()
    debug(pub.__dict__)
    e = db_session.query(IngestionLog).first()
    debug(e.args)
    publications = db_session.query(WoSPublication)

    assert publications.count() == 1


@pytest.mark.asyncio
async def test_ingest_zip(db_session):
    filename = "tests/test_data/web_of_science/1967/1967_CORE.zip"
    res = await wos_treat_zip(filename)
    debug(res)
    assert False


@pytest.mark.asyncio
async def test_wos_bugged(db_session):
    testdata_dir = "tests/test_data/web_of_science/"
    filename = f"{testdata_dir}WR_2022_20220225152855_CORE_0001.xml"
    ns = "{http://clarivate.com/schema/wok5.30/public/FullRecord}"
    record_el_iterator = etree.iterparse(filename, tag=f"{ns}REC")

    bugged = [
        2090,
        8933,
        13035,
        19367,
        30388,
        36605,
        37067,
        38987,
        39179,
        51573,
    ]
    i = 0
    errors = 0
    for _, record_el in record_el_iterator:
        i += 1
        if i in bugged:
            try:
                _ = await wos_ingest_one(record_el)
            except Exception as e:
                errors += 1
                debug(i, e.args)

    publications = db_session.query(WoSPublication)
    authors = db_session.query(WoSAuthor)
    authorships = db_session.query(WoSAuthorship)

    debug(publications.count(), authors.count(), authorships.count())
    for au in authors:
        debug(au.name)
    assert False


@pytest.mark.asyncio
async def test_wos_bigfile(db_session):

    testdata_dir = "tests/test_data/web_of_science/"
    filename = f"{testdata_dir}WR_2022_20220225152855_CORE_0001.xml"
    ns = "{http://clarivate.com/schema/wok5.30/public/FullRecord}"
    record_el_iterator = etree.iterparse(filename, tag=f"{ns}REC")

    start = time.perf_counter()
    MAX_PUB = -1
    i = 0
    res = []
    errors = 0
    for event, record_el in record_el_iterator:
        i += 1
        try:
            new = await wos_ingest_one(record_el)
            res.append(new)
        except Exception as e:
            errors += 1
            with open("BUG.txt", "a") as f:
                f.write(f"\n\n\n\n\n{i}\n\n{e.args}\n\n")
                f.write(str(xml_to_dict(record_el)))
        # if i==MAX_PUB:
        #    break
    stop = time.perf_counter()

    print(f"Res:\t{res}")
    print("\n")
    print(f"Time:\t{stop-start}")
    print("\n")

    publications = db_session.query(WoSPublication)
    authors = db_session.query(WoSAuthor)
    authorships = db_session.query(WoSAuthorship)
    errors = db_session.query(IngestionLog)

    print(f"Publications:\t{publications.count()}")
    print(f"Authors:\t{authors.count()}")
    print(f"Authorships:\t{authorships.count()}")
    print(f"Errors:\t{errors}")
    assert publications.count() == MAX_PUB


@pytest.mark.asyncio
async def test_wos_mass_ingestion(db_session):

    dir = "tests/test_data/fake_wos/"

    start = time.perf_counter()
    res = await wos_ingest_dir(dir)
    stop = time.perf_counter()

    debug(res)
    total_time = stop - start

    publications = db_session.query(WoSPublication)
    authors = db_session.query(WoSAuthor)
    authorships = db_session.query(WoSAuthorship)
    errors = db_session.query(IngestionLog)

    PRINT = True
    if PRINT:
        print(f"Result:\t{res}")
        print(f"Time:\t{total_time}")
        print(f"Publications:\t{publications.count()}")
        print(f"Authors:\t{authors.count()}")
        print(f"Authorships:\t{authorships.count()}")
        print(f"Errors:\t{errors.count()}")

    WRITE = False
    if WRITE:
        with open(f"{dir}results.txt", "w") as f:
            f.write(f"Result:\t{res}")
            f.write(f"Time:\t{total_time}")
            f.write(f"Publications:\t{publications.count()}")
            f.write(f"Authors:\t{authors.count()}")
            f.write(f"Authorships:\t{authorships.count()}")
            f.write(f"Errors:\t{errors.count()}")

    # search for all authors whose name starts with "A" and who published
    # something befor 1955
    query = (
        authors.filter(WoSAuthor.name.startswith("A"))
        .join(WoSAuthorship)
        .filter(WoSAuthorship.author_id == WoSAuthor.id)
        .join(WoSPublication)
        .filter(WoSPublication.publication_year < 1955)
    )
    print(query.count())

    for e in errors:
        print(e)

    assert False


@pytest.mark.asyncio
async def test_abstract(db_session):
    data_dir = "tests/test_data/web_of_science"
    zipfile = "2022_ESCI.zip"

    publications = db_session.query(WoSPublication)
    assert publications.count() == 0

    await wos_treat_zip(f"{data_dir}/{zipfile}")
    assert publications.count() == 0
    assert False
