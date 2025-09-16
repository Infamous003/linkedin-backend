from pydantic import BaseModel
from ..models.models import Status
from datetime import datetime


class PostPublic(BaseModel):
    id: int
    user_id: int

    title: str
    body: str
    status: Status

    impressions: int
    created_at: datetime
    scheduled_at: datetime | None = None


class PostCreate(BaseModel):
    title: str
    body: str 
    scheduled_at: datetime | None = None
    

class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    scheduled_at: datetime | None = None
