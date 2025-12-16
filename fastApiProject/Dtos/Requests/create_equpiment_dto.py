from pydantic import BaseModel


class CreateEquipmentDto(BaseModel):
    name: str
    image_path: str | None = None
