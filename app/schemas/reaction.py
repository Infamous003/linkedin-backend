from pydantic import BaseModel
from ..models.models import ReactionType
from datetime import datetime


class ReactionBase(BaseModel):
    type: ReactionType

class ReactionPublic(BaseModel):
    id: int
    type: ReactionType
    post_id: int
    user_id: int
    created_at: datetime