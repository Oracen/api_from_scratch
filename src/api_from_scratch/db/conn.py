import json
from typing import Any, Dict, List, Union
from pathlib import Path

from api_from_scratch.constants import FILEPATH_DB


class Conn:
    def __init__(self, filepath: Union[str, Path] = FILEPATH_DB) -> None:
        """
        DB Connection spoofer path, used to emulate a proper backend

        Args:
            filepath: path to specify the location of the local testing data to
                serve until actual data can be acquired.
        """
        self.filepath = Path(filepath)

    def init_db(self) -> None:
        """
        Checks for the existence of a 'db' file and creates one if none found
        """
        if self.filepath.exists():
            raise ValueError("Database is already initialised!")
        data: Dict[str, List[Any]] = {"users": [], "items": []}
        with open(self.filepath, "w") as f:
            json.dump(data, f)

    def clear_db(self) -> None:
        """
        Deletes the DB, only used for testing purposes
        """
        self.filepath.unlink(missing_ok=True)


def load_db(path: Path) -> Conn:
    db_conn = Conn(path)
    try:
        # Allow for existing DB
        db_conn.init_db()
    except ValueError:
        pass
    return db_conn
