from database.models import Bookings
from app.schemas.booking_schemas import BookingCreate
from sqlalchemy.orm import Session
from database.db_enum import BookingStatusEnum
from fastapi.responses import JSONResponse
from fastapi import status
def create_booking(db: Session,create_booking:BookingCreate):
    new_booking = Bookings(
        customer_id=create_booking.customer_id,
        provider_id=create_booking.provider_id,
        booking_date=create_booking.booking_date,
        service_id=create_booking.service_id,
        status=BookingStatusEnum.Pending,
    )
    db.add(new_booking)
    db.commit()
    db.flush()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Bookings created successfully",
            "data" :{
                "booking_id" : new_booking.id
                },
        }
    )