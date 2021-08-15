from pydantic.main import BaseModel


class PostItem(BaseModel):
    id: int
    text: str
