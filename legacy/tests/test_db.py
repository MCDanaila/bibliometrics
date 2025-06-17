from devtools import debug


def test_db_connection(db_session):
    assert db_session is not None
    debug(db_session)
