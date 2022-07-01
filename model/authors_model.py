from pydantic import BaseModel

class Author(BaseModel):
    id: int = None
    name: str = None
    picture: int = None
    papers: int = None
