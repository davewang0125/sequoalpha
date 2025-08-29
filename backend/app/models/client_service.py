from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

from ..database import Base

class ClientService(Base):
    __tablename__ = "client_services"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    
    # Service details
    status = Column(String, nullable=False, default="active")  # active, completed, cancelled
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    
    # Progress tracking
    current_step = Column(Integer, default=0)  # índice del paso actual
    progress_percentage = Column(Float, default=0.0)  # 0.0 a 100.0
    
    # Deliverables and history
    entregables = Column(JSON, default=list)  # Lista de objetos: {nombre, ruta, fecha, comentarios}
    historial_cambios = Column(JSON, default=list)  # Lista de cambios/comentarios
    
    # Additional info
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("User", back_populates="client_services")
    service = relationship("Service") 