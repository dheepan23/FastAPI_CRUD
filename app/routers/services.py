from app.services.service_service import create_service
from fastapi import APIRouter,Depends,status,HTTPException
from app.schemas.service_schemas import ServiceCreate,ServiceResponse
from database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/services",tags=["Services"])
@router.post("/create_service",response_model=ServiceResponse)
def service_create(service:ServiceCreate,db:Session = Depends(get_db)):
    try:
        return create_service(db,service)
    except HTTPException as e:
        raise e
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creatig the service",
        )