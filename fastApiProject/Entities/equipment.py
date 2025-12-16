from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=True)

    items = relationship("EquipmentItem", back_populates="equipment")
