from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response
import os
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_current_admin, get_db, get_current_user
from ..models.client_service import ClientService
from ..schemas.client_service import ClientServiceCreate, ClientServiceOut, Entregable
from ..crud import client_service as crud_client_service
from ..crud import user as crud_user
from ..crud import service as crud_service

router = APIRouter(prefix="/client-services", tags=["client-services"])

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/assign-service", response_model=ClientServiceOut)
def assign_service_to_client(
    user_id: int,
    service_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Asignar un servicio a un cliente (solo admin)"""
    # Verificar que el usuario existe
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que el servicio existe
    service = crud_service.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    # Verificar que no esté ya asignado
    existing_assignment = crud_client_service.get_client_service(db, user_id, service_id)
    if existing_assignment:
        raise HTTPException(status_code=400, detail="Este servicio ya está asignado al cliente")
    
    # Crear la asignación
    client_service_data = ClientServiceCreate(
        user_id=user_id,
        service_id=service_id,
        estado="pendiente",
        progreso="0%"
    )
    
    return crud_client_service.create_client_service(db, client_service_data)

@router.get("/client/{user_id}", response_model=List[ClientServiceOut])
def get_client_services(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los servicios de un cliente (solo el propio cliente o admin)"""
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver estos servicios")
    
    return crud_client_service.get_client_services_by_user(db, user_id)

@router.put("/{client_service_id}/progress")
def update_service_progress(
    client_service_id: int,
    progreso: str,
    estado: str = None,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Actualizar el progreso de un servicio (solo admin)"""
    client_service = crud_client_service.get_client_service_by_id(db, client_service_id)
    if not client_service:
        raise HTTPException(status_code=404, detail="Servicio del cliente no encontrado")
    
    return crud_client_service.update_progress(db, client_service_id, progreso, estado)

@router.post("/upload-entregable/")
def upload_entregable(
    user_id: int,
    service_id: int,
    file: UploadFile = File(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Subir archivo de entregable (solo admin)"""
    
    # Validar extensión
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")
    
    # Validar tamaño
    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande (máx 10MB)")
    
    # Renombrar archivo
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = file.filename.replace(" ", "_")
    new_filename = f"cliente_{user_id}_{now}_{safe_name}"
    user_folder = f"uploads/cliente_{user_id}"
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, new_filename)
    
    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Actualizar entregables en ClientService
    client_service = crud_client_service.get_client_service(db, user_id, service_id)
    if not client_service:
        raise HTTPException(status_code=404, detail="Servicio del cliente no encontrado")
    
    # Crear objeto entregable
    entregable = Entregable(
        nombre=new_filename,
        ruta=file_path,
        fecha=datetime.now(),
        comentarios=None
    )
    
    # Actualizar entregables
    entregables = client_service.entregables or []
    entregables.append(entregable.dict())
    client_service.entregables = entregables
    db.commit()
    db.refresh(client_service)
    
    return {"filename": new_filename, "ruta": file_path, "entregables": entregables}

@router.get("/my-entregables/{service_id}")
def list_my_entregables(service_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Listar entregables del usuario actual para un servicio específico"""
    client_service = crud_client_service.get_client_service(db, current_user.id, service_id)
    if not client_service:
        raise HTTPException(status_code=404, detail="Servicio del cliente no encontrado")
    return {"entregables": client_service.entregables or []}

@router.get("/download-entregable/{user_id}/{filename}")
def download_entregable(user_id: int, filename: str, current_user=Depends(get_current_user)):
    """Descargar un entregable (solo el dueño o admin)"""
    
    # Solo permite descargar si el usuario es el dueño o admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para descargar este archivo")
    
    file_path = os.path.join(f"uploads/cliente_{user_id}", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    with open(file_path, "rb") as f:
        content = f.read()
    
    # Detectar tipo de archivo para el header
    ext = filename.split(".")[-1].lower()
    content_type = "application/pdf" if ext == "pdf" else f"image/{ext}"
    
    return Response(content, media_type=content_type, headers={"Content-Disposition": f"attachment; filename={filename}"}) 

@router.post("/test-upload")
def test_upload(
    file: UploadFile = File(...),
    current_admin=Depends(get_current_admin)
):
    """Endpoint temporal para probar subida de archivos"""
    try:
        # Validar extensión
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")
        
        # Validar tamaño
        contents = file.file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Archivo demasiado grande (máx 10MB)")
        
        # Guardar archivo temporal
        test_folder = "uploads/test"
        os.makedirs(test_folder, exist_ok=True)
        file_path = os.path.join(test_folder, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {
            "success": True,
            "filename": file.filename,
            "size": len(contents),
            "path": file_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)} 

@router.post("/simulate-upload/{user_id}/{service_id}")
def simulate_upload(
    user_id: int,
    service_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Simular subida de entregable sin archivo (para pruebas)"""
    try:
        # Verificar que el cliente tiene el servicio
        client_service = crud_client_service.get_client_service(db, user_id, service_id)
        if not client_service:
            raise HTTPException(status_code=404, detail="Servicio del cliente no encontrado")
        
        # Crear entregable simulado
        now = datetime.now()
        entregable = {
            "nombre": f"entregable_simulado_{now.strftime('%Y%m%d_%H%M%S')}.txt",
            "ruta": f"uploads/cliente_{user_id}/entregable_simulado.txt",
            "fecha": now.isoformat(),
            "comentarios": "Entregable simulado para pruebas"
        }
        
        # Actualizar entregables
        entregables = client_service.entregables or []
        entregables.append(entregable)
        client_service.entregables = entregables
        db.commit()
        db.refresh(client_service)
        
        return {
            "success": True,
            "entregable": entregable,
            "total_entregables": len(entregables)
        }
    except Exception as e:
        return {"success": False, "error": str(e)} 