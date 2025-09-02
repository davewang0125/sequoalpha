from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

from ..database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    base_price = Column(Float, nullable=False)  # precio por cm²
    pasos_flujo = Column(JSON, nullable=False, default=list)  # Lista de pasos en JSON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 