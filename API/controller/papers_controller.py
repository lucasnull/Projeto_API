from fastapi import APIRouter, Header, Body, Request
from typing import List, Union
from API.database.database import BaseDAO
from API.model.papers_model import Paper
from API.database.security import get_user, get_user_admin
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
databaseDAO = BaseDAO()
limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])


@router.get("/list-papers", response_model=List[Paper])
@limiter.limit("5/minute")
async def list_papers(request: Request, token: Union[str, None] = Header(default=None)):
    get_user(token)
    paper = None
    list_paper = []
    records = (databaseDAO.select_value('SELECT * FROM bancoproj.papers'))
    for row in records:
        author = Paper(paper_id=row[0], category=row[1], title=row[2], summary=row[3], first_paragraph=row[4], body=row[5], authors_id=row[6])
        list_paper.append(author)
    return list_paper


@router.post("/new-paper")
@limiter.limit("5/minute")
async def add_paper(request: Request, new_paper: Paper, token: str = Header(default=None)):
    get_user_admin(token)
    record = (new_paper.category, new_paper.title, new_paper.summary, new_paper.first_paragraph, new_paper.body, new_paper.authors_id)
    user = databaseDAO.create_value('''INSERT INTO bancoproj.papers(paper_id, category, title, summary, first_paragraph, body, authors_id) VALUES (%s, %s, %s, %s, %s, %s, %s)''',record)
    if user == 1:
        return "Paper inserido com Sucesso!!"
    else:
        return "Falha na inserção"


@router.patch("/update-paper")
@limiter.limit("5/minute")
async def update_author(request: Request, id: int, token: str = Header(default=None), update_paper_dto: Paper = Body(default=None)):
    get_user_admin(token)
    user = databaseDAO.patch_value(
        (f"UPDATE bancoproj.papers SET category = '{update_paper_dto.category}', title = '{update_paper_dto.title}', summary = '{update_paper_dto.summary}', first_paragraph = '{update_paper_dto.first_paragraph}', body = '{update_paper_dto.body}', authors_id = '{update_paper_dto.authors_id}' WHERE paper_id = {id}"))
    if user == 1:
        return "Registro atualizado com Sucesso!!"
    else:
        return "Falha na atualização"