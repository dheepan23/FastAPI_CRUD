from app.services.booking_service import create_booking
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database.database import get_db
from app.schemas.booking_schemas import BookingCreate,BookingResponse,BookingUpdate
from database.models import Bookings
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/bookings",tags=["Bookings"])

@router.post("/create_booking",response_model=BookingResponse)
def create_bookings(booking:BookingCreate,db:Session = Depends(get_db)):
    try:
        return create_booking(db,booking)
    except HTTPException as e:
        raise e
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the booking",
        )

@router.get("/get_booking",response_model=BookingResponse)
def get_booking_id(booking_id:int,db:Session = Depends(get_db)):
    try:
        booking = db.query(Bookings).filter(Bookings.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message" : "Booking retrieved successfully",
                "data" : booking
            }
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the booking",
        )
    
@router.put("/update_booking",response_model=BookingResponse)
def update_booking_id(booking_update: BookingUpdate,db:Session=Depends(get_db)):
    try:
        booking = db.query(Bookings).filter(Bookings.id == booking_update.id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        if booking_update.provider_id:
            booking.provider_id = booking_update.provider_id
        if booking_update.service_id:
            booking.service_id = booking_update.service_id
        if booking_update.status:
            booking.status = booking_update.status
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content="Booking updated successfully",
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the booking",
        )
    
@router.delete("delete_booking")
def delete_booking_id(booking_id: int,db:Session=Depends(get_db)):
    try:
        booking = db.query(Bookings).filter(Bookings.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        db.delete(booking)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Booking deleted successfully",
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the booking",
        )