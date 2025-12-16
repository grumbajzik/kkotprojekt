from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class EquipmentItem(Base):
    __tablename__ = "equipment_item"

    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))

    equipment = relationship("Equipment", back_populates="items")
    reservations = relationship("EquipmentItemReservation", back_populates="item")
    comments = relationship("Comment", back_populates="equipment_item")
