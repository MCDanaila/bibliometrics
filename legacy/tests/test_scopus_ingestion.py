import time
from pathlib import Path

import pytest
from devtools import debug
from psycopg2._psycopg import ProgrammingError

from libbiblio.db.models.maintenance import IngestionLog
from libbiblio.db.models.scopus import ScopusAbstract
from libbiblio.db.models.scopus import ScopusAffiliation
from libbiblio.db.models.scopus import ScopusAuthor
from libbiblio.db.models.scopus import ScopusAuthorship
from libbiblio.db.models.scopus import ScopusPublication
from libbiblio.db.models.scopus import ScopusSource
from libbiblio.sources.scopus.scopus_ingestor import scopus_ingest_dir
from libbiblio.sources.scopus.scopus_ingestor import scopus_ingest_one
from libbiblio.sources.scopus.scopus_ingestor import scopus_treat_zip


test_data_folder = Path(__file__).parent / "test_data/scopus"


@pytest.mark.asyncio
async def test_scopus_ingest_dir(db_session):
    dir = "tests/test_data/scopus/tmp/2-s2.0-84874133732.xml"
    res = await scopus_ingest_one(dir, "", "")
    debug(res)
    # publications = db_session.query(ScopusPublication)
    # authors = db_session.query(ScopusAuthor)
    # authorships = db_session.query(ScopusAuthorship)
    # debug(res, publications.count(), authors.count(), authorships.count())
    # for pub in publications:
    #    debug(pub.title)
    assert True


@pytest.mark.asyncio
async def test_bug(db_session):
    path = "bugged_files"
    fname = "2-s2.0-0021592689.xml"
    ret = await scopus_ingest_one(f"{path}/{fname}", path, fname)

    logs = db_session.query(IngestionLog)
    if logs.count() > 0:
        debug(logs.first().__dict__["args"])
    debug(ret)
    debug(db_session.query(ScopusPublication).first().__dict__)
    debug(db_session.query(ScopusAuthor).all())
    assert False


@pytest.mark.asyncio
async def test_scopus_40pubs_ingestion_publications(db_session):
    """
    Using a limited number to speed up the test.
    """
    all_files = test_data_folder.as_posix()
    await scopus_ingest_dir(all_files)
    assert db_session.query(ScopusPublication).count() == 42


@pytest.mark.asyncio
async def test_ingest_dir(db_session):

    dir_path = "tests/test_data/scopus/zip/prova"

    start = time.perf_counter()
    try:
        res = await scopus_ingest_dir(dir_path)
    except ProgrammingError as e:
        print(str(e))

    stop = time.perf_counter()

    total_time = stop - start

    publications = db_session.query(ScopusPublication)
    authors = db_session.query(ScopusAuthor)
    authorships = db_session.query(ScopusAuthorship)
    errors = db_session.query(IngestionLog)

    PRINT = True
    if PRINT:
        print(f"Result:\t{res}")
        print(f"Time:\t{total_time}")
        print(f"Publications:\t{publications.count()}")
        print(f"Authors:\t{authors.count()}")
        print(f"Authorships:\t{authorships.count()}")
        print(f"Errors:\t{errors.count()}")

    with open("error_20M.txt", "w") as f:

        f.write(f"Result:\t{res}\n")
        f.write(f"Time:\t{total_time}\n")
        f.write(f"Publications:\t{publications.count()}\n")
        f.write(f"Authors:\t{authors.count()}\n")
        f.write(f"Authorships:\t{authorships.count()}\n")

        f.write(10 * "\n")
        f.write(f"Errors:\t{errors.count()}\n")
        f.write("\n")

        for e in errors:
            f.write(str(e))
            f.write("\n")

    assert False


@pytest.mark.asyncio
async def test_ingest_zip(db_session):

    dir_path = "tests/test_data/scopus/zip/2020-12-3_ANI_0143-xml-11.zip"

    start = time.perf_counter()
    try:
        res = await scopus_treat_zip(dir_path)
    except ProgrammingError as e:
        print("Eccolo")
        print(str(e))
    stop = time.perf_counter()

    total_time = stop - start

    publications = db_session.query(ScopusPublication)
    authors = db_session.query(ScopusAuthor)
    authorships = db_session.query(ScopusAuthorship)
    errors = db_session.query(IngestionLog)

    PRINT = True
    if PRINT:
        print(f"Result:\t{res}")
        print(f"Time:\t{total_time}")
        print(f"Publications:\t{publications.count()}")
        print(f"Authors:\t{authors.count()}")
        print(f"Authorships:\t{authorships.count()}")
        print(f"Errors:\t{errors.count()}")

    for e in errors:
        debug(e)

    assert False


@pytest.mark.asyncio
async def test_delete(db_session):

    source = ScopusSource(name="PubMed")

    author1 = ScopusAuthor(given_name="Mario")
    author2 = ScopusAuthor(given_name="Luigi")
    author3 = ScopusAuthor(given_name="Waluigi")

    affiliation1 = ScopusAffiliation(organization="Sissa")
    affiliation2 = ScopusAffiliation(organization="UniTs")

    publication1 = ScopusPublication(
        title="La pizza", source=source, scpid=1993
    )
    publication2 = ScopusPublication(title="La pasta", source=source, scpid=42)

    authorship1 = ScopusAuthorship(
        author=author1, affiliation=affiliation1, publication=publication1
    )
    authorship2 = ScopusAuthorship(
        author=author2, affiliation=affiliation2, publication=publication1
    )
    authorship3 = ScopusAuthorship(
        author=author2, affiliation=affiliation2, publication=publication2
    )
    authorship4 = ScopusAuthorship(
        author=author3, affiliation=affiliation2, publication=publication2
    )

    db_session.add(authorship1)
    db_session.add(authorship2)
    db_session.add(authorship3)
    db_session.add(authorship4)
    db_session.commit()

    assert db_session.query(ScopusSource).count() == 1
    assert db_session.query(ScopusPublication).count() == 2
    assert db_session.query(ScopusAuthor).count() == 3
    assert db_session.query(ScopusAffiliation).count() == 2
    assert db_session.query(ScopusAuthorship).count() == 4

    debug(db_session.query(ScopusPublication.scpid).all())

    scpid_to_delete = 42

    q = db_session.query(ScopusPublication).filter(
        ScopusPublication.scpid == scpid_to_delete
    )

    id_to_delete = q.first().id

    db_session.query(ScopusAuthorship).filter(
        ScopusAuthorship.publication_id == id_to_delete
    ).delete()

    q.delete()

    assert db_session.query(ScopusSource).count() == 1
    assert db_session.query(ScopusPublication).count() == 1
    assert db_session.query(ScopusAuthor).count() == 3
    assert db_session.query(ScopusAffiliation).count() == 2
    assert db_session.query(ScopusAuthorship).count() == 2

    debug(db_session.query(ScopusPublication.scpid).all())


@pytest.mark.asyncio
async def test_abstract(db_session):
    abstract = ScopusAbstract(text="prova")
    publication = ScopusPublication(scpid=1, sgrid=1, abstract=abstract)
    db_session.add(publication)
    db_session.commit()
    assert db_session.query(ScopusAbstract).count() == 1
    pub = (
        db_session.query(ScopusPublication)
        .filter(ScopusPublication.scpid == 1)
        .first()
    )
    debug(pub.abstract_id, pub.abstract)
    assert False
