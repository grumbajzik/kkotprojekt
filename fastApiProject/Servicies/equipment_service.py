from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from Entities import Equipment, EquipmentItem
from Repositories import equipment_repository, equipment_item_repository


class EquipmentService:

    def __init__(self, db: Session):
        self.db = db

    def create_equipment(self, name: str):
        return equipment_repository.create_equipment(self.db, name)

    def update_equipment(self, equipment_id: int, name: str):
        equipment = equipment_repository.get_equipment_by_id(self.db, equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")
        return equipment_repository.update_equipment(self.db, equipment, name)

    def delete_equipment(self, equipment_id: int):
        equipment = equipment_repository.get_equipment_by_id(self.db, equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")
        equipment_repository.delete_equipment(self.db, equipment)

    def add_item(self, equipment_id: int):
        equipment = equipment_repository.get_equipment_by_id(self.db, equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")
        return equipment_item_repository.create_item(self.db, equipment_id)
