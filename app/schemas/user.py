from pydantic import BaseModel
from ..models.models import Role

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    role: Role = Role.USER

class UserPublic(BaseModel):
    firstname: str
    lastname: str
    username: str
    role: Role

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    password: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str