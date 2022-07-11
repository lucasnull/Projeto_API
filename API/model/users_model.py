from pydantic import BaseModel, Field, validator
import re
from API.database.security import get_password_hash


class User(BaseModel):
    hash_password: str = Field(alias='password')
    type: str = None
    email: str = None
    username: str = None

    @validator('hash_password', pre=True)
    def hash_the_password(cls, v):
        return get_password_hash(v)

    @validator('email')
    def validate_email_format(cls, v):
        if not re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+').match(v):
            raise ValueError('The user email format is invalid!')
        return v
