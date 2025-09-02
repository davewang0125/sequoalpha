from fastapi import APIRouter, Depends
from ..schemas.user import UserOut
from ..dependencies import get_current_user
from ..dependencies import get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user 

@router.get("/admin-only")
def admin_only(current_admin = Depends(get_current_admin)):
    return {"message": f"Hola, admin {current_admin.name}!"} 