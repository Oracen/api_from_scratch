import random

from fastapi.testclient import TestClient

from api_from_scratch.api.main import app
from api_from_scratch.api.fixed_returns import API_VERSIONS
from api_from_scratch.structs.external.user import User
from api_from_scratch.structs.internal.post_item import PostItem
from tests.helpers.base_api_tests import BaseAPITest

client = TestClient(app)

valid_header = "acceptable"

# TODO: Most of this base functionality is repeated, refactor into default testing
# class for CRUD of major API branches


class TestRoots:
    def test_get_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "OK", "versions": API_VERSIONS}

    def test_apiv1_get_root(self):
        response = client.get("/v1/")
        assert response.status_code == 200
        assert response.json() == {"message": ""}


class TestV1Users(BaseAPITest):
    route = "/v1/users"
    id_key = "id"
    item1: User = User(id=random.randint(10, 10000000), name="Test User")
    item2: User = User(id=random.randint(10, 10000000), name="User Test")
    modify_items = [("name", "str")]


class TestV1Items(BaseAPITest):
    route = "/v1/items"
    id_key = "id"
    item1 = PostItem(
        id=random.randint(10, 10000000), text="Kourban Dallas was a famous character"
    )
    item2 = PostItem(
        id=random.randint(10, 10000000), text="One man rode the night train"
    )
    modify_items = [("text", "str")]
