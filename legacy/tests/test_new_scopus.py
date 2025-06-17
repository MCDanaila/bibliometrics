from pathlib import Path

from devtools import debug  # type: ignore

from libbiblio.db.models import *  # noqa:F405
from libbiblio.sources.scopus.scopus_ingestor import scopus_ingest_dir
from libbiblio.sources.scopus.scopus_ingestor import scopus_ingest_zip

test_data_folder = Path(__file__).parent / "test_data/scopus"


def test_ingest_dir(db):

    if 1:
        path = f"{str(test_data_folder)}/zip"
        zipname = "2022-7-13_ANI_0323-xml-7.zip"
        scopus_ingest_zip(zipname, path)

    # Export bugged files
    if 0:
        import os
        import zipfile

        zip_filename = (
            f"{str(test_data_folder)}/zip/2022-7-13_ANI_0323-xml-7.zip"
        )
        bugged_files = [x[0] for x in db.query(IngestionLog.xml_name).all()]

        if not os.path.exists(f"{str(test_data_folder)}/bugged"):
            os.makedirs(f"{str(test_data_folder)}/bugged")

        with zipfile.ZipFile(zip_filename) as zip_file:
            for file_name in bugged_files:
                zip_file.extract(file_name, f"{str(test_data_folder)}/bugged")

    if 0:
        path = f"{str(test_data_folder)}/zip"
        debug(path)
        scopus_ingest_dir(str(path))

    if 0:
        for e in db.query(IngestionLog):
            debug(e)

    if 0:
        debug(db.query(ScopusPublication).count())
        debug(db.query(ScopusSource).count())
        debug(db.query(ScopusAffiliation).count())
        debug(db.query(ScopusAuthor).count())
        debug(db.query(ScopusAuthorship).count())
        debug(db.query(ScopusCitation).count())
        debug(db.query(NotLinkedScopusCitation).count())
        debug(db.query(IngestionLog).count())

    assert True
