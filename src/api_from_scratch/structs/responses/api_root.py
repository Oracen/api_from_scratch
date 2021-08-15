from typing import List
from pydantic import BaseModel


class ResponseApiRoot(BaseModel):
    message: str
    versions: List[str]
