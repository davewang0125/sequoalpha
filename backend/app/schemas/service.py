from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

class PasoFlujo(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None  # pendiente, en_progreso, finalizado, etc.

class ServiceBase(BaseModel):
    name: str
    description: str
    base_price: float
    pasos_flujo: List[Dict[str, Any]]  # Lista de pasos en JSON
    is_active: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 