from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class OrderStatusEnum(str, Enum):
    PENDING = "pendiente"
    UPLOADED = "archivo_subido"
    REVIEWING = "en_revision"
    APPROVED = "aprobado"
    IN_PRODUCTION = "en_produccion"
    COMPLETED = "completado"
    SHIPPED = "enviado"
    DELIVERED = "entregado"
    CANCELLED = "cancelado"

class PaymentStatusEnum(str, Enum):
    PENDING = "pendiente"
    PAID = "pagado"
    FAILED = "fallido"
    REFUNDED = "reembolsado"

class PrintOrderBase(BaseModel):
    material_type: str = Field(..., description="Tipo de madera para la impresión")
    dimensions: Dict[str, float] = Field(..., description="Dimensiones en formato {width, height, depth}")
    quantity: int = Field(1, ge=1, description="Cantidad de piezas")
    print_style: str = Field(..., description="Estilo de impresión")
    color_preferences: Optional[Dict[str, Any]] = Field(None, description="Preferencias de color")
    contact_name: str = Field(..., min_length=2, description="Nombre de contacto")
    contact_email: str = Field(..., description="Email de contacto")
    contact_phone: Optional[str] = Field(None, description="Teléfono de contacto")
    shipping_address: str = Field(..., min_length=10, description="Dirección de envío")
    customer_notes: Optional[str] = Field(None, description="Notas del cliente")

    @validator('dimensions')
    def validate_dimensions(cls, v):
        required_keys = ['width', 'height', 'depth']
        if not all(key in v for key in required_keys):
            raise ValueError('Las dimensiones deben incluir width, height y depth')
        if any(v[key] <= 0 for key in required_keys):
            raise ValueError('Todas las dimensiones deben ser mayores a 0')
        return v

    @validator('contact_email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Email inválido')
        return v

class PrintOrderCreate(PrintOrderBase):
    file_name: str = Field(..., description="Nombre del archivo")
    file_size: Optional[int] = Field(None, description="Tamaño del archivo en bytes")

class PrintOrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    payment_status: Optional[PaymentStatusEnum] = None
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    internal_notes: Optional[str] = None

class PrintOrderResponse(PrintOrderBase):
    id: int
    user_id: int
    file_name: str
    file_path: str
    file_size: Optional[int]
    status: OrderStatusEnum
    payment_status: PaymentStatusEnum
    total_price: float
    tax_amount: float
    shipping_cost: float
    created_at: datetime
    updated_at: Optional[datetime]
    estimated_delivery: Optional[datetime]
    actual_delivery: Optional[datetime]
    tracking_number: Optional[str]
    tracking_updates: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True

class OrderProgressCreate(BaseModel):
    status: OrderStatusEnum
    description: str = Field(..., min_length=5, description="Descripción del progreso")

class OrderProgressResponse(BaseModel):
    id: int
    order_id: int
    status: OrderStatusEnum
    description: str
    created_at: datetime
    updated_by: Optional[int]

    class Config:
        from_attributes = True

class TrackingUpdate(BaseModel):
    status: str = Field(..., description="Estado del envío")
    location: Optional[str] = Field(None, description="Ubicación actual")
    description: str = Field(..., description="Descripción del update")
    timestamp: datetime = Field(default_factory=datetime.now)

class PrintOrderWithProgress(PrintOrderResponse):
    progress_updates: List[OrderProgressResponse] = []

    class Config:
        from_attributes = True
