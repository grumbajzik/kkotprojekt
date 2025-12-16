from pydantic import BaseModel


class CreateEquipmentItemDto(BaseModel):
    equipment_id: int
