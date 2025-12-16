from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class EquipmentItemReservation(Base):
    __tablename__ = "equipment_item_reservation"

    equipment_item_id = Column(Integer, ForeignKey("equipment_item.id"), primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservation.id"), primary_key=True)

    item = relationship("EquipmentItem", back_populates="reservations")
    reservation = relationship("Reservation", back_populates="items")
