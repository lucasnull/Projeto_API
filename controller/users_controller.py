from fastapi import APIRouter, HTTPException, Header, Body
from typing import List, Union
from database.database import BaseDAO
from database.security import verify_password, create_token, get_user
from model.users_model import User
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
databaseDAO = BaseDAO()
limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])


@router.get("/list-users", response_model=List[User])
@limiter.limit("5/minute")
async def list_users(token: Union[str, None] = Header(default=None)):
    get_user(token)
    user = None
    list_user = []
    records = (databaseDAO.select_value('SELECT * FROM bancoproj.users'))
    for row in records:
        user = User(id=row[0], password=row[1], type=row[2], email=row[3], username=row[4])
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
async def delete_user(id: int, token: Union[str, None] = Header(default=None)):
    get_user(token)
    records = databaseDAO.delete_value('DELETE FROM bancoproj.users WHERE id = %s', id)
    if records == 1:
        return "Registro deletado com Sucesso!!"
    else:
        return "Falha na deleção"

@router.post("/login")
async def login(username: str, password: str):
    db_user = (databaseDAO.select_value(f"SELECT * FROM bancoproj.users WHERE username='{username}'"))
    valid_password = verify_password(password, db_user[0][1])
    if username != db_user[0][4]:
        raise HTTPException(status_code=401, detail="Usuário não registrado!!!")
    if not valid_password:
        raise HTTPException(status_code=401, detail="Senha incorreta!!!")
    else:
        list = [
            username,
            db_user[0][2]
        ]
    return {
        "token": create_token(list)
    }

@router.patch("/update-user")
async def update_user(id: int, token: str = Header(default=None), update_user_dto: User = Body(default=None)):
    get_user(token)
    user = databaseDAO.patch_value(
        (f"UPDATE bancoproj.users SET hash_password = '{update_user_dto.hash_password}', type = '{update_user_dto.type}', email = '{update_user_dto.email}', username = '{update_user_dto.username}' WHERE id = {id}"))
    if user == 1:
        return "Registro atualizado com Sucesso!!"
    else:
        return "Falha na atualização"
