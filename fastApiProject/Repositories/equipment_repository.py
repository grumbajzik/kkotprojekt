from sqlalchemy.orm import Session
from Entities import Equipment


def create_equipment(db: Session, name: str, file: str | None = None):
    equipment = Equipment(name=name)
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


def get_all_equipment(db: Session):
    return db.query(Equipment).all()


def get_equipment_by_id(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()


def update_equipment(db: Session, equipment: Equipment, name: str):
    equipment.name = name
    db.commit()
    db.refresh(equipment)
    return equipment


def delete_equipment(db: Session, equipment: Equipment):
    db.delete(equipment)
    db.commit()
