from pathlib import Path

from api_from_scratch.constants import FILEPATH_DB_TESTING
from api_from_scratch.db.conn import load_db


def test_db_initial_create() -> None:
    """
    Check to see DB can be initialized
    """
    path = Path(FILEPATH_DB_TESTING)
    if path.is_file():
        path.unlink()
    db_conn = load_db(FILEPATH_DB_TESTING)
    assert db_conn.filepath.is_file()


def test_db_duplicate_create() -> None:
    """
    Check that consecutive initializations fail
    """
    db_conn = load_db(FILEPATH_DB_TESTING)
    try:
        db_conn.init_db()
    except ValueError:
        return

    raise ValueError("This test should return in the above exception")


def test_db_destroy() -> None:
    """
    Check teardown of DB
    """
    db_conn = load_db(FILEPATH_DB_TESTING)
    db_conn.clear_db()
    assert not db_conn.filepath.is_file()
