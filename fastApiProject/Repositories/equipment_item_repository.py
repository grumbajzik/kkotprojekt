from sqlalchemy.orm import Session
from Entities import EquipmentItem


def create_item(db: Session, equipment_id: int):
    item = EquipmentItem(equipment_id=equipment_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: EquipmentItem):
    db.delete(item)
    db.commit()
