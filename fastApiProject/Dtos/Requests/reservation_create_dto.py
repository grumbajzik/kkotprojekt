from pydantic import BaseModel
from typing import List
from datetime import date


class CreateReservationDto(BaseModel):
    equipment_item_ids: List[int]
    reservation_date: date
