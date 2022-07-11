from pydantic import BaseModel

class Author(BaseModel):
    name: str = None
    picture: int = None
