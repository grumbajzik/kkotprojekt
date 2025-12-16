import os

from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from Auth.Dependencies import get_current_user, approver_only
from Dtos.Requests.create_equipment_item_dto import CreateEquipmentItemDto
from Dtos.Requests.create_equpiment_dto import CreateEquipmentDto
from Dtos.Requests.update_equipment_dto import UpdateEquipmentDto
from Entities import User
from database import get_db
from Servicies.equipment_service import EquipmentService


router = APIRouter(
    prefix="/equipment",
    tags=["Vybavení"]
)


def get_service(db: Session = Depends(get_db)):
    return EquipmentService(db)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_equipment(
    name: str = Form(...),
    image: UploadFile = File(None),
    service: EquipmentService = Depends(get_service),
    user: User = Depends(get_current_user)
):
    approver_only(user)
    image_path = None
    if image:
        upload_dir = "uploaded_images"
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, image.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
    dto = CreateEquipmentDto(name=name, image_path=image_path)
    return service.create_equipment(dto)


@router.put("/{equipment_id}")
def update_equipment(
    equipment_id: int,
    dto: UpdateEquipmentDto,
    service: EquipmentService = Depends(get_service),
    user: User = Depends(get_current_user)
):
    approver_only(user)
    return service.update_equipment(equipment_id, dto.name)


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(
    equipment_id: int,
    service: EquipmentService = Depends(get_service),
    user: User = Depends(get_current_user)
):
    approver_only(user)
    service.delete_equipment(equipment_id)


@router.post("/items")
def add_item(
    dto: CreateEquipmentItemDto,
    service: EquipmentService = Depends(get_service),
    user: User = Depends(get_current_user)
):
    approver_only(user)
    return service.add_item(dto.equipment_id)