import random

from api_from_scratch.constants import FILEPATH_DB_TESTING
from api_from_scratch.crud.post_item import CRUDItem
from api_from_scratch.crud.user import CRUDUser
from api_from_scratch.db.conn import load_db
from api_from_scratch.structs.external.user import User
from api_from_scratch.structs.internal.post_item import PostItem
from tests.helpers.base_crud_tests import BaseCrudTests


class TestUser(BaseCrudTests):
    id_key = "id"
    conn_obj = load_db(FILEPATH_DB_TESTING.parent / "test_user.json")
    item1: User = User(id=random.randint(10000, 10000000), name="Test User")
    item2: User = User(id=random.randint(10000, 10000000), name="User Test")
    citem = CRUDUser(conn_obj)
    modify_items = [("name", "str")]


class TestItem(BaseCrudTests):
    id_key = "id"
    conn_obj = load_db(FILEPATH_DB_TESTING.parent / "test_item.json")
    item1 = PostItem(id=random.randint(10000, 10000000), text="One long string")
    item2 = PostItem(
        id=random.randint(10000, 10000000), text="A somewhat longer string"
    )
    citem = CRUDItem(conn_obj)
    modify_items = [("text", "str")]
