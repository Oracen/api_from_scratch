from fastapi import APIRouter, HTTPException
from api_from_scratch.db.conn import load_db
from api_from_scratch.structs.internal.post_item import PostItem

from api_from_scratch.structs.responses.v1_item import ResponseV1Item
from api_from_scratch.crud.post_item import CRUDItem
from api_from_scratch.constants import FILEPATH_DB

router = APIRouter()
db_conn = load_db(FILEPATH_DB)
crud_item = CRUDItem(db_conn)

_404 = HTTPException(404, "Resources not found")
# TODO: Logging


@router.get("")
def get_all_items():
    items = crud_item.read_all({})
    return ResponseV1Item(server_code=200, items=items)


@router.put("", status_code=201)
def put_item(item: PostItem):
    response = crud_item.create(item)
    if response == 201:
        return ResponseV1Item(server_code=201, items=[])
    elif response == 409:
        raise HTTPException(409, "Resource already exists")
    else:
        raise _404


@router.get("/{item_id}")
def get_item(item_id: int):
    item = crud_item.read({"id": item_id})
    if len(item) == 1:
        return ResponseV1Item(
            server_code=200,
            items=[item[0]],
        )
    else:
        raise _404


@router.delete("/{item_id}")
def delete_item(item_id: int):
    response = crud_item.delete(item_id)
    if response == 200:
        return ResponseV1Item(server_code=201, items=[])
    else:
        raise _404


@router.patch("")
def update_item(item: PostItem):
    response = crud_item.update(item)
    if response == 200:
        return ResponseV1Item(server_code=200, items=[])
    else:
        raise _404
