from fastapi import APIRouter

from api_from_scratch.api.v1.root import router as router_root
from api_from_scratch.api.v1.items import router as router_items
from api_from_scratch.api.v1.users import router as router_users

router_v1 = APIRouter()

router_v1.include_router(router_root, tags=["root"])
router_v1.include_router(router_items, prefix="/items", tags=["items"])
router_v1.include_router(router_users, prefix="/users", tags=["users"])
