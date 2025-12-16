from pydantic import BaseModel
from datetime import datetime


class CommentDto(BaseModel):
    id: int
    text: str
    created_at: datetime
