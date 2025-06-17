from pathlib import Path

from devtools import debug  # type: ignore

from libbiblio.db.models import *  # noqa:F405
from libbiblio.sources.wos.wos_ingestor import wos_ingest_dir


test_data_folder = Path(__file__).parent / "test_data/wos/small"


def test_ingest_dir(db):

    if 1:
        wos_ingest_dir(str(test_data_folder))

    if 1:
        for e in db.query(IngestionLog).limit(20):
            debug(e)

    if 1:
        debug(db.query(WoSPublication).count())
        debug(db.query(WoSSource).count())
        debug(db.query(WoSAffiliation).count())
        debug(db.query(WoSAuthor).count())
        debug(db.query(WoSAuthorship).count())
        debug(db.query(WoSCitation).count())
        debug(db.query(NotLinkedWoSCitation).count())
        debug(db.query(IngestionLog).count())
