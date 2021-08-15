from typing import List
from api_from_scratch.structs.internal.post_item import PostItem
from .api_v1 import ResponseV1


class ResponseV1Item(ResponseV1):
    items: List[PostItem]
