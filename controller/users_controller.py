from fastapi import APIRouter
from typing import List
from database.database import BaseDAO
from model.users_model import User

router = APIRouter()
databaseDAO = BaseDAO()


@router.get("/list-users", response_model=List[User])
async def list_users():
    user = None
    list_user = []
    records = (databaseDAO.select_value('SELECT * FROM bancoproj.users'))
    for row in records:
        user = User(id=row[0], hash_password=row[1], type=row[2], email=row[3], username=row[4])
        list_user.append(user)
    return list_user

@router.post("/new-user")
async def add_user(new_user: User):
    record = (new_user.hash_password, new_user.type, new_user.email, new_user.username)
    user = databaseDAO.create_value('''INSERT INTO bancoproj.users(hash_password, type, email, username) VALUES (%s, %s, %s, %s)''',record)
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
