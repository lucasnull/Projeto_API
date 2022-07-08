from datetime import datetime, timedelta
import os
from typing import Any, Union
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from database.database import BaseDAO
import json

databaseDAO = BaseDAO()
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

SECRET_KEY = os.getenv('SECRET_KEY', 'Jv9anY5ZM!AR8&g8gb!93b94$dSJjKQ$XD$$RGRmDRWedjKaVo')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS512')
ACCESS_TOKEN_EXPIRE_HOURS = 0.2
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def get_user(token=Depends(oauth2_schema)):
    try:
        username = decode_token(token)[0]
        type = decode_token(token)[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid Token!!!")
    # se tiver um token vai verificar se tem um username
    if not username:
        raise HTTPException(status_code=401, detail="Invalid Token!!!")
    # se tiver um username vai verificar se tem no banco e for admin
    if type == 'admin':
        db_user = (databaseDAO.select_value(f"SELECT * FROM bancoproj.users WHERE username='{username}'"))
    else:
        raise HTTPException(status_code=400, detail="User has not access!!!")

    return db_user


def decode_token(token: str):
    decoding = jwt.decode(token, SECRET_KEY, algorithms=['HS512'])
    return decoding.get("sub").replace("'", "").strip('][').split(', ')

def create_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS512')
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
