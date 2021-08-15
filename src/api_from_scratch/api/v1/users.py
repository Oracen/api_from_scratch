from fastapi import APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from api_from_scratch.db.conn import load_db
from api_from_scratch.structs.external.user import User

from api_from_scratch.structs.responses.v1_user import ResponseV1User
from api_from_scratch.crud.user import CRUDUser
from api_from_scratch.constants import FILEPATH_DB

router = APIRouter()
db_conn = load_db(FILEPATH_DB)
crud_user = CRUDUser(db_conn)

_404 = HTTPException(404, "Resources not found")
# TODO: Logging


@router.get("")
def get_all_items(request: Request):
    items = crud_user.read_all({})
    return ResponseV1User(server_code=200, items=items)


@router.put("", status_code=201)
def put_item(item: User):
    response = crud_user.create(item)
    if response == 201:
        return ResponseV1User(server_code=201, items=[])
    elif response == 409:
        raise HTTPException(409, "Resource already exists")
    else:
        raise _404


@router.get("/{item_id}")
def get_item(item_id: int):
    item = crud_user.read({"id": item_id})
    if len(item) == 1:
        return ResponseV1User(
            server_code=200,
            items=[item[0]],
        )
    else:
        raise _404


@router.delete("/{item_id}")
def delete_item(item_id: int):
    response = crud_user.delete(item_id)
    if response == 200:
        return ResponseV1User(server_code=201, items=[])
    else:
        raise _404


@router.patch("")
def update_item(item: User):
    response = crud_user.update(item)
    if response == 200:
        return ResponseV1User(server_code=200, items=[])
    else:
        raise _404
