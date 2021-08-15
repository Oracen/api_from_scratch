import random
import string

from typing import Any, List, Tuple

from pydantic.main import BaseModel

from api_from_scratch.constants import FILEPATH_DB_TESTING
from api_from_scratch.crud.base import CRUDBase
from api_from_scratch.db.conn import Conn, load_db

from api_from_scratch.structs.placeholders import EmptyBaseModel


class BaseCrudTests(object):
    conn_obj = load_db(FILEPATH_DB_TESTING.parent / "test.json")
    item1: Any = EmptyBaseModel()
    item2: Any = EmptyBaseModel()
    id_key: str = "id"
    modify_items: List[Tuple[str, str]] = []
    citem = CRUDBase(conn_obj)

    subst_string = "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(random.randint(5, 20))
    )
    subst_number = random.randint(10, 10000000)

    def test_class_init(self):
        assert type(self.conn_obj) == Conn
        assert type(self.item1) == type(self.item2)
        assert issubclass(type(self.item1), BaseModel)
        assert issubclass(type(self.citem), CRUDBase)
        assert self.id_key != ""

    def test_create_success(self):
        code = self.citem.create(self.item1)
        assert code == 201

    def test_read_success(self):
        item_id = getattr(self.item1, self.id_key)
        item = self.citem.read({self.id_key: item_id})
        assert len(item) == 1
        assert getattr(item[0], self.id_key) == item_id

    def test_create_fail(self):
        code = self.citem.create(self.item1)
        assert code == 409

    def test_read_fail(self):
        item = self.citem.read({self.id_key: getattr(self.item2, self.id_key)})
        assert len(item) == 0

    def test_update(self):
        for key, typ in self.modify_items:
            BaseClass = self.item1.__class__
            item_mod = self.item1.dict().copy()
            if typ == "str":
                value = self.subst_string
            elif typ == "int":
                value = self.subst_number
            elif typ == "float":
                value = self.subst_string / random.randint(5, 100)
            else:
                raise NotImplementedError(
                    f"Type {typ} does not currently have implementation."
                )
            item_mod[key] = value
            self.citem.update(BaseClass(**item_mod))
            item = self.citem.read({self.id_key: getattr(self.item1, self.id_key)})[0]
            assert getattr(item, key) == value

    def test_read_all(self):
        self.citem.update(self.item2)
        items = self.citem.read_all({})
        assert len(items) == 2

        items = self.citem.read({self.id_key: getattr(self.item1, self.id_key)})
        assert len(items) == 1

    def test_delete(self):
        self.citem.delete(getattr(self.item1, self.id_key))
        items = self.citem.read_all({})
        assert len(items) == 1

        self.citem.delete(getattr(self.item2, self.id_key))
        items = self.citem.read_all({})
        assert len(items) == 0

    def test_clear_db(self):
        self.conn_obj.clear_db()
        assert not self.conn_obj.filepath.is_file()
