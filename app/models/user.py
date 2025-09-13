from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__="users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=32, min_length=8, unique=True, nullable=False)
    firstname: str = Field(max_length=32, min_length=1, nullable=False)
    lastname: str = Field(max_length=32, min_length=1, nullable=False)
    password: str = Field(max_length=128, min_length=12, nullable=False)

    role: Role = Field(default=Role.USER, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    