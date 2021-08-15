from typing import List
from api_from_scratch.structs.external.user import User
from .api_v1 import ResponseV1


class ResponseV1User(ResponseV1):
    items: List[User]
