from pydantic import BaseModel
from datetime import datetime
from database.db_enum import BookingStatusEnum
from typing import Optional

class BookingBase(BaseModel):
    customer_id: int
    provider_id: int
    booking_date: datetime
    service_id: int
    status: Optional[BookingStatusEnum] = BookingStatusEnum.Pending


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int

    class Config:
        from_attributes = True
class BookingUpdate(BaseModel):
    booking_id : int
    provider_id : Optional[int]
    service_id : Optional[int]
    status : Optional[BookingStatusEnum]