from fastapi import APIRouter
from typing import List
from database.database import BaseDAO
from model.authors_model import Author

router = APIRouter()
databaseDAO = BaseDAO()


@router.get("/list-authors", response_model=List[Author])
async def list_authors():
    author = None
    list_author = []
    records = (databaseDAO.select_value('SELECT * FROM bancoproj.authors'))
    for row in records:
        author = Author(id=row[0], hash_password=row[1], type=row[2], email=row[3], username=row[4])
        list_author.append(author)
    return list_author

@router.post("/new-user")
async def add_user(new_user: User):
    record = (new_user.id, new_user.hash_password, new_user.type, new_user.email, new_user.username)
    user = databaseDAO.create_value('''INSERT INTO bancoproj.users(id, hash_password, type, email, username) VALUES (%s, %s, %s, %s, %s)''',record)
    if user == 1:
        return "Registro inserido com Sucesso!!"
    else:
        return "Falha na inserção"

@router.delete("/delete-user")
async def delete_user(id: int):
    records = databaseDAO.delete_value('DELETE FROM bancoproj.users WHERE id = %s', id)
    if records == 1:
        return "Registro deletado com Sucesso!!"
    else:
        return "Falha na deleção"