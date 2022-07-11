from pydantic import BaseModel

class Paper(BaseModel):
    category: str = None
    title: str = None
    summary: str = None
    first_paragraph: str = None
    body: str = None
    authors_id: int = None
