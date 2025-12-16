from pydantic import BaseModel


class RejectReservationDto(BaseModel):
    reason: str
