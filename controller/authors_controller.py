from fastapi import APIRouter, Header, Body, Request
from typing import List, Union
from database.database import BaseDAO
from model.authors_model import Author
from database.security import verify_password, create_token, get_user, get_user_admin
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
databaseDAO = BaseDAO()
limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])


@router.get("/list-authors", response_model=List[Author])
@limiter.limit("5/minute")
async def list_authors(request: Request, token: Union[str, None] = Header(default=None)):
    get_user(token)
    author = None
    list_author = []
    records = (databaseDAO.select_value('SELECT * FROM bancoproj.authors'))
    for row in records:
        author = Author(id=row[0], hash_password=row[1], type=row[2], email=row[3], username=row[4])
        list_author.append(author)
    return list_author


@router.post("/new-author")
@limiter.limit("5/minute")
async def add_author(request: Request, new_author: Author, token: str = Header(default=None)):
    get_user_admin(token)
    record = (new_author.hash_password, new_author.type, new_author.email, new_author.username)
    user = databaseDAO.create_value('''INSERT INTO bancoproj.users(hash_password, type, email, username) VALUES (%s, %s, %s, %s)''',record)
    if user == 1:
        return "Author inserido com Sucesso!!"
    else:
        return "Falha na inserção"


@router.patch("/update-author")
@limiter.limit("5/minute")
async def update_author(request: Request, token: str = Header(default=None), update_user_dto: Author = Body(default=None)):
    get_user_admin(token)
    user = databaseDAO.patch_value(
        (f"UPDATE bancoproj.users SET hash_password = '{update_user_dto.hash_password}', type = '{update_user_dto.type}', email = '{update_user_dto.email}', username = '{update_user_dto.username}' WHERE id = {id}"))
    if user == 1:
        return "Registro atualizado com Sucesso!!"
    else:
        return "Falha na atualização"