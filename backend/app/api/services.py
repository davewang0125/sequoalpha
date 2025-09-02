from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from ..schemas.service import ServiceCreate, ServiceOut
from ..crud import service as crud_service
from ..dependencies import get_current_admin, get_db

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=ServiceOut)
def create_service(
    service: ServiceCreate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Crear un nuevo servicio (solo admin)"""
    return crud_service.create_service(db, service)

@router.get("/", response_model=List[ServiceOut])
def list_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar todos los servicios disponibles (público)"""
    services = crud_service.get_services(db, skip=skip, limit=limit)
    return services

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    """Obtener un servicio específico por ID (público)"""
    service = crud_service.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return service

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    service: ServiceCreate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Actualizar un servicio (solo admin)"""
    db_service = crud_service.get_service(db, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return crud_service.update_service(db, service_id, service)

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Eliminar un servicio (solo admin)"""
    db_service = crud_service.get_service(db, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    crud_service.delete_service(db, service_id)
    return {"message": "Servicio eliminado correctamente"} 