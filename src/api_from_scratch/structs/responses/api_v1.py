from typing import Any, List
from pydantic import BaseModel


class ResponseV1(BaseModel):
    version: str = "v1"
    items: List[Any]
    server_code: int
