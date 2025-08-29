from sqlalchemy.orm import Session
from ..models.client_service import ClientService
from ..schemas.client_service import ClientServiceCreate
from datetime import datetime

def create_client_service(db: Session, client_service: ClientServiceCreate):
    db_client_service = ClientService(
        user_id=client_service.user_id,
        service_id=client_service.service_id,
        estado=client_service.estado,
        progreso=client_service.progreso,
        entregables=client_service.entregables,
        historial_cambios=client_service.historial_cambios
    )
    db.add(db_client_service)
    db.commit()
    db.refresh(db_client_service)
    return db_client_service

def get_client_service(db: Session, user_id: int, service_id: int):
    return db.query(ClientService).filter(
        ClientService.user_id == user_id,
        ClientService.service_id == service_id
    ).first()

def get_client_service_by_id(db: Session, client_service_id: int):
    return db.query(ClientService).filter(ClientService.id == client_service_id).first()

def get_client_services_by_user(db: Session, user_id: int):
    return db.query(ClientService).filter(ClientService.user_id == user_id).all()

def update_progress(db: Session, client_service_id: int, progreso: str, estado: str = None):
    client_service = db.query(ClientService).filter(ClientService.id == client_service_id).first()
    if client_service:
        client_service.progreso = progreso
        if estado:
            client_service.estado = estado
        
        # Agregar al historial de cambios
        cambio = {
            "fecha": datetime.now().isoformat(),
            "descripcion": f"Progreso actualizado a {progreso}",
            "usuario": "admin"
        }
        
        historial = client_service.historial_cambios or []
        historial.append(cambio)
        client_service.historial_cambios = historial
        client_service.fecha_ultimo_cambio = datetime.now()
        
        db.commit()
        db.refresh(client_service)
    
    return client_service

def get_all_client_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClientService).offset(skip).limit(limit).all() 