from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"))
    equipment_item_id = Column(Integer, ForeignKey("equipment_item.id"))
    reservation_id = Column(Integer, ForeignKey("reservation.id"))

    user = relationship("User", back_populates="comments")
    equipment_item = relationship("EquipmentItem", back_populates="comments")
    reservation = relationship("Reservation", back_populates="comments")
