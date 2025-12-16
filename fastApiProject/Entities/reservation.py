from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime
from .base import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)
    reservation_date = Column(DateTime, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    approved_date = Column(DateTime, nullable=True)
    returned_date = Column(DateTime, nullable=True)
    order_number = Column(Integer, default=0)

    customer_id = Column(Integer, ForeignKey("user.id"))
    approver_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    approved = Column(Boolean, default=False)
    cancelled = Column(Boolean, default=False)

    items = relationship("EquipmentItemReservation", back_populates="reservation")
    comments = relationship("Comment", back_populates="reservation")
