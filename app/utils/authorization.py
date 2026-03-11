from fastapi import Depends, HTTPException
from app.utils.jwt_handler import get_current_user
from database.models import Users

def admin_required(current_user: Users = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

def customer_required(current_user: Users = Depends(get_current_user)):
    if current_user.role.value != "customer":
        raise HTTPException(
            status_code=403,
            detail="Customer access required"
        )
    return current_user