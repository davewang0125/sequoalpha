from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from ..database import get_db
from ..dependencies import get_current_user
from ..models.user import User
from ..models.print_order import OrderStatus, PaymentStatus
from ..schemas.print_order import (
    PrintOrderCreate, PrintOrderResponse, PrintOrderUpdate, 
    OrderProgressCreate, OrderProgressResponse, PrintOrderWithProgress
)
from ..crud.print_order import print_order_crud

router = APIRouter(prefix="/print-orders", tags=["print-orders"])

# Configuración para archivos
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".pdf", ".ai", ".eps", ".cdr"}

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

def validate_file_extension(filename: str) -> bool:
    """Validar extensión del archivo"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

@router.post("/upload-file", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Subir archivo para impresión"""
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de archivo no permitido. Formatos válidos: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Guardar archivo
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al guardar el archivo")
    
    return {
        "file_name": file.filename,
        "file_path": file_path,
        "file_size": len(content),
        "message": "Archivo subido exitosamente"
    }

@router.post("/", response_model=PrintOrderResponse)
async def create_print_order(
    order_data: PrintOrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva orden de impresión"""
    # Verificar que el archivo existe
    if not os.path.exists(order_data.file_path):
        raise HTTPException(status_code=400, detail="Archivo no encontrado")
    
    # Crear la orden
    db_order = print_order_crud.create_order(
        db=db,
        order_data=order_data,
        user_id=current_user.id,
        file_path=order_data.file_path
    )
    
    return db_order

@router.get("/", response_model=List[PrintOrderResponse])
async def get_user_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las órdenes del usuario actual"""
    orders = print_order_crud.get_user_orders(db, current_user.id, skip, limit)
    return orders

@router.get("/{order_id}", response_model=PrintOrderWithProgress)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener una orden específica con su progreso"""
    order = print_order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Verificar que el usuario es dueño de la orden o es admin
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver esta orden")
    
    # Obtener progreso
    progress = print_order_crud.get_order_progress(db, order_id)
    
    # Crear respuesta con progreso
    response = PrintOrderWithProgress.from_orm(order)
    response.progress_updates = [OrderProgressResponse.from_orm(p) for p in progress]
    
    return response

@router.get("/{order_id}/file")
async def download_order_file(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Descargar el archivo de una orden"""
    order = print_order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Verificar permisos
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para descargar este archivo")
    
    if not os.path.exists(order.file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        order.file_path,
        filename=order.file_name,
        media_type="application/octet-stream"
    )

@router.put("/{order_id}", response_model=PrintOrderResponse)
async def update_order(
    order_id: int,
    order_update: PrintOrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar una orden (solo admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden actualizar órdenes")
    
    order = print_order_crud.update_order(db, order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    return order

@router.post("/{order_id}/progress", response_model=OrderProgressResponse)
async def add_progress_update(
    order_id: int,
    progress_data: OrderProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Agregar actualización de progreso (solo admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden agregar progreso")
    
    # Verificar que la orden existe
    order = print_order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    progress = print_order_crud.create_progress(
        db=db,
        order_id=order_id,
        status=progress_data.status,
        description=progress_data.description,
        updated_by=current_user.id
    )
    
    return progress

@router.get("/{order_id}/progress", response_model=List[OrderProgressResponse])
async def get_order_progress(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener historial de progreso de una orden"""
    order = print_order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Verificar permisos
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver el progreso")
    
    progress = print_order_crud.get_order_progress(db, order_id)
    return progress

# Endpoints para administradores
@router.get("/admin/all", response_model=List[PrintOrderResponse])
async def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las órdenes (solo admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden ver todas las órdenes")
    
    orders = print_order_crud.get_all_orders(db, skip, limit)
    return orders

@router.get("/admin/status/{status}", response_model=List[PrintOrderResponse])
async def get_orders_by_status(
    status: OrderStatus,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener órdenes por estado (solo admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden filtrar por estado")
    
    orders = print_order_crud.get_orders_by_status(db, status, skip, limit)
    return orders

@router.get("/admin/payment/{payment_status}", response_model=List[PrintOrderResponse])
async def get_orders_by_payment_status(
    payment_status: PaymentStatus,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener órdenes por estado de pago (solo admin)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden filtrar por estado de pago")
    
    orders = print_order_crud.get_orders_by_payment_status(db, payment_status, skip, limit)
    return orders
