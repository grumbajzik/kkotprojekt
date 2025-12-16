from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from .comment_dto import CommentDto


class ReservationDto(BaseModel):
    id: int
    item_id: int
    user_id: int
    start_date: datetime
    end_date: datetime
    approved: bool
    note: str | None = None
    approver_id: int | None = None
    reject_reason: str | None = None
    created_at: datetime
    updated_at: datetime
    comments: List[CommentDto] = []