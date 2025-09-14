from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from .enums import Role, Status
from functools import partial

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=32, min_length=8, unique=True, nullable=False)
    firstname: str = Field(max_length=32, min_length=1, nullable=False)
    lastname: str = Field(max_length=32, min_length=1, nullable=False)
    password: str = Field(max_length=128, min_length=12, nullable=False)
    role: Role = Field(default=Role.USER, nullable=False)
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))

    posts: list["Post"] = Relationship(back_populates="user")  # plural for one-to-many


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    title: str = Field(max_length=100, min_length=16, nullable=False)
    body: str = Field(min_length=100, nullable=False)
    status: Status = Field(default=Status.PUBLISHED, nullable=False)
    scheduled_at: datetime | None = Field(default=None, nullable=True)
    impressions: int = Field(default=0)
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))

    user: User = Relationship(back_populates="posts")  # singular for many-to-one
