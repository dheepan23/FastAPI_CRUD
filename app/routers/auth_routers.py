from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.authentication_schemas import LoginSchema

from database.database import get_db
from app.services.auth_services import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    try:
        return login_user(db, data.email, data.password)

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while login",
        )