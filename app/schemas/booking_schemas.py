from pydantic import BaseModel
from datetime import datetime
from database.db_enum import BookingStatusEnum


class BookingBase(BaseModel):
    customer_id: int
    provider_id: int
    booking_date: datetime
    service_id: int
    status: BookingStatusEnum


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int

    class Config:
        from_attributes = True