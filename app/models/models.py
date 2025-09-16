from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from datetime import datetime, timezone
from .enums import Role, Status, ReactionType
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
    reactions: list["Reaction"] = Relationship(back_populates="user")


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
    reactions: list["Reaction"] = Relationship(back_populates="post")


class Reaction(SQLModel, table=True):
    __tablename__ = "reactions"
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uq_post_user_reaction"),)

    id: int | None = Field(default=None, primary_key=True)
    post_id: int | None = Field(foreign_key="posts.id", nullable=False)
    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    type: ReactionType = Field(nullable=False)
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))

    post: Post = Relationship(back_populates="reactions")
    user: User = Relationship(back_populates="reactions")