from typing import Any, Dict, List, Optional
from api_from_scratch.db.conn import Conn
from api_from_scratch.structs.external.user import User
from api_from_scratch.crud.base import CRUDBase


class CRUDUser(CRUDBase):
    _db_table = "users"

    def __init__(self, db_conn: Conn) -> None:
        """
        CRUD class for any user data
        """
        super().__init__(db_conn)
        self.db_conn = db_conn
        self.check_init()

    def create(self, user: User) -> int:
        data = self.open()
        if any([user.id == i[self._id_key] for i in data[self._db_table]]):
            return 409
        else:
            data[self._db_table].append(user.dict())
            self.save(data)
            return 201

    # Devnote: Using for-loop instead of index as defining suitably flexible
    # __eq__ is impractical, and a full filter system is for when an actual sql
    # interface is built

    def read(self, filter_dict: Dict[str, Any]) -> List[User]:
        data = self.open()
        for item in data[self._db_table]:
            match = [item[key] == value for key, value in filter_dict.items()]
            if all(match):
                return [User(**item)]
        return []

    def update(self, user: User) -> int:
        data = self.open()
        found = False
        for i, item in enumerate(data[self._db_table]):
            if user.id == item[self._id_key]:
                found = True
                break

        user_new = user.dict()
        if found:
            data[self._db_table][i] = user_new
        else:
            data[self._db_table].append(user_new)
        data[self._db_table]
        self.save(data)
        return 200

    def read_all(self, filter_dict: Dict[str, Any]) -> List[User]:
        data = self.open()
        if len(filter_dict.items()) == 0:
            return [User(**i) for i in data[self._db_table]]
        const = []
        for item in data[self._db_table]:
            match = [item[key] == value for key, value in filter_dict.items()]
            if all(match):
                const.append(User(**item))
        return const

    def delete(self, user_id: int) -> int:
        data = self.open()
        for i, item in enumerate(data[self._db_table]):
            if user_id == item[self._id_key]:
                found = True
                break
        if found:
            data[self._db_table].pop(i)
            self.save(data)
            return 200
        else:
            return 404
