from pydantic import BaseModel


class ReturnReservationDto(BaseModel):
    comment: str
