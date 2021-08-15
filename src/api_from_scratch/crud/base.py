import json
from typing import Any, Dict, List

from api_from_scratch.db.conn import Conn


class CRUDBase:
    _db_table = "ABSTRACT_BASE"
    _id_key = "id"

    def __init__(self, db_conn: Conn) -> None:
        """
        This is the abstract base class to enforce consistent object behaviour
        on all CRUD operations.

        Default behaviour

        Arguments:
            db_conn: the object used, in whatever way, to establish connections
                to the database. For now, its a JSON
        """
        self.db_conn = db_conn

    def open(self) -> Dict[str, Any]:
        with open(self.db_conn.filepath, "r") as f:
            return json.load(f)

    def save(self, data: Dict[str, Any]) -> None:
        with open(self.db_conn.filepath, "w") as f:
            json.dump(data, f)

    def create(self, obj: Any) -> int:
        """
        If no record exists, create it
        """
        raise NotImplementedError()

    def read(self, filter_dict: Dict[str, Any]) -> List[Any]:
        """
        For a read call, normally there would be some optional SQL filters. For
        this DB simulator, I'm instead going to treat the object passed in init
        as a set of filters for simplicity

        Returns to this function should be unique attributes like keys

        Arguments:
            filter_dict: dictionary of attr name and value pairs to match against
                db entries
        """
        raise NotImplementedError()

    def read_all(self, filter_dict: Dict[str, Any]) -> List[Any]:
        """
        This is a softer matching system capable of returning anything with a
        complete match.

        Arguments:
            filter_dict: dictionary of attr name and value pairs to match against
                db entries. An empty dictionary {} as an argument will instead
                list all entries
        """
        raise NotImplementedError()

    def update(self, obj: Any) -> int:
        """
        Updates the object specified
        """
        raise NotImplementedError()

    def delete(self, obj: Any) -> int:
        """
        Deletes the object specified
        """
        raise NotImplementedError()

    def check_init(self) -> int:
        """
        Quick helper which can be used to check status of connections etc. on
        class init
        """
        data = self.open()
        try:
            data[self._db_table]
        except KeyError:
            data[self._db_table] = []
            self.save(data)
        return 200
