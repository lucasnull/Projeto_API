from pydantic import BaseModel

class Paper(BaseModel):
    id: int = None
    category: str = None
    title: str = None
    summary: str = None
    firstParagraph: str = None
    body: str = None
    author_id: int = None
