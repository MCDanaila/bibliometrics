from devtools import debug

from libbiblio.db.models.scopus import ScopusCitation
from libbiblio.db.models.scopus import ScopusPublication


def test_scopus_model(db_session):
    citing = ScopusPublication()
    cited = ScopusPublication()
    p = ScopusPublication()
    p.citations.append(citing)
    p.bibliography.append(cited)
    debug(p)

    db_session.add_all([citing, cited, p])
    db_session.commit()

    assert db_session.query(ScopusPublication).count() == 3
    assert db_session.query(ScopusCitation).count() == 2
