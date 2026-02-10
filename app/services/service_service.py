from database.models import Services
from app.schemas.service_schemas import ServiceCreate,ServiceResponse
from sqlalchemy.orm import Session
from database.models import Services
from fastapi.responses import JSONResponse
from fastapi import status

def create_service(db:Session,service:ServiceCreate):
    new_service = Services(
            name=service.name,
            description=service.description,
            price=service.price,
            duration_minutes=service.duration_minutes
        )
    db.add(new_service)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Service created successfully",
    )