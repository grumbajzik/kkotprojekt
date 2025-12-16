from pydantic import BaseModel


class UpdateEquipmentDto(BaseModel):
    name: str