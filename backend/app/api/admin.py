from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.user import UserCreate, UserOut
from ..schemas.print_order import PrintOrderResponse
from ..crud import user as crud_user
from ..crud import print_order as crud_print_order
from ..dependencies import get_db, get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/create-admin", response_model=UserOut)
def create_admin_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Endpoint temporal para crear usuarios admin"""
    db_user = crud_user.get_user_by_email(db, user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear usuario con rol admin
    db_user = crud_user.create_admin_user(db, user_in)
    return db_user

@router.get("/orders", response_model=List[PrintOrderResponse])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtener todas las órdenes (solo admin)"""
    orders = crud_print_order.print_order_crud.get_all_orders(db, skip, limit)
    return orders

@router.get("/users", response_model=List[UserOut])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtener todos los usuarios (solo admin)"""
    users = crud_user.get_users(db, skip, limit)
    return users 