from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_approver = Column(Boolean, default=False)

    comments = relationship("Comment", back_populates="user")
    customer_reservations = relationship("Reservation", foreign_keys="Reservation.customer_id")
    approver_reservations = relationship("Reservation", foreign_keys="Reservation.approver_id")
