from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class Entregable(BaseModel):
    nombre: str
    ruta: str  # Ruta o URL del archivo
    fecha: Optional[datetime] = None
    comentarios: Optional[str] = None

class Cambio(BaseModel):
    fecha: datetime
    descripcion: str
    usuario: str  # nombre o id del usuario que hizo el cambio

class ClientServiceBase(BaseModel):
    user_id: int
    service_id: int
    estado: Optional[str] = "pendiente"
    progreso: Optional[str] = None
    entregables: List[Entregable] = []
    historial_cambios: List[Cambio] = []

class ClientServiceCreate(ClientServiceBase):
    pass

class ClientServiceOut(ClientServiceBase):
    id: int
    fecha_inicio: datetime
    fecha_ultimo_cambio: Optional[datetime] = None

    class Config:
        from_attributes = True 