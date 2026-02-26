from database.models import Services
from app.schemas.service_schemas import ServiceCreate,ServiceResponse
from sqlalchemy.orm import Session
from database.models import Services
from fastapi.responses import JSONResponse
from fastapi import status,HTTPException

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

def get_services(db:Session,service_id):
    service = db.query(Services).filter(Services.id ==service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Service retrieved successfully",
            "data":{
                "service_id" :  service.id,
                "name" : service.name,
                "is_active" : service.is_active,
                "description" : service.description,
                },
        }
    )