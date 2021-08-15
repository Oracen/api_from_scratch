import random
import string
from typing import List, Tuple

from fastapi.testclient import TestClient
from pydantic import BaseModel
from requests.models import Response

from api_from_scratch.api.main import app

from api_from_scratch.structs.placeholders import EmptyBaseModel
from api_from_scratch.structs.responses.api_v1 import ResponseV1


def assert_status(response: Response, http_code: int):
    r = response.status_code
    assert r == http_code, f"Expected: {http_code} , Received: {r}"


class BaseAPITest(object):

    client = TestClient(app)
    route = ""
    item1: BaseModel
    item2: BaseModel
    id_key = ""
    subst_string = "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(random.randint(5, 20))
    )
    subst_number = random.randint(10, 10000000)
    modify_items: List[Tuple[str, str]] = []

    def test_class_init(self):
        assert self.route != ""
        assert issubclass(type(self.item1), BaseModel)
        assert issubclass(type(self.item2), BaseModel)
        assert self.item1.dict() != {}
        assert self.item2.dict() != {}
        assert self.id_key != ""

    def test_write_delete(self):
        response = self.client.put(self.route, json=self.item1.dict())
        assert_status(response, 201)
        response = self.client.put(self.route, json=self.item1.dict())
        assert_status(response, 409)
        response = self.client.delete(
            f"{self.route}/{getattr(self.item1, self.id_key)}"
        )
        assert_status(response, 200)

    def test_data_check(self):
        item_id = getattr(self.item1, self.id_key)
        self.client.put(self.route, json=self.item1.dict())
        response = self.client.get(f"{self.route}/{item_id}")
        assert_status(response, 200)
        assert response.json()["items"][0] == self.item1.dict()
        response = self.client.delete(f"{self.route}/{item_id}")
        assert_status(response, 200)

    def test_edit(self):
        item_id = getattr(self.item1, self.id_key)
        data = self.item1.dict()
        self.client.put(self.route, json=data)
        for key, typ in self.modify_items:
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
            data[key] = value
            response = self.client.patch(f"{self.route}", json=data)
            assert_status(response, 200)
            response = self.client.get(f"{self.route}/{item_id}")
            assert_status(response, 200)
            assert response.json()["items"][0][key] == value
        response = self.client.delete(f"{self.route}/{item_id}")
        assert_status(response, 200)

    def test_getall(self):
        self.client.put(self.route, json=self.item1.dict())
        response = self.client.put(self.route, json=self.item2.dict())
        assert_status(response, 201)
        response = self.client.get(self.route)
        assert_status(response, 200)
        assert len(response.json()["items"]) == 2

    def test_cleanup(self):
        response = self.client.get(self.route)
        assert_status(response, 200)
        for item in response.json()["items"]:
            self.client.delete(f"{self.route}/{item[self.id_key]}")
        response = self.client.get(self.route)
        assert_status(response, 200)
        n_items = len(response.json()["items"])
        assert n_items == 0, "Should have 0 items, instead has {n_items}"
