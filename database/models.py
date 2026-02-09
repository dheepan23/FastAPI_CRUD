from sqlalchemy import Column,Integer,String,Boolean,Float,DateTime,ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database.database import Base
from database.db_enum import UserTypeEnum,BookingStatusEnum

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50),nullable=False)
    email = Column(String(50),unique=True,index=True,nullable=False)
    hashed_password = Column(String(50),nullable=False)
    role = Column(SQLAlchemyEnum(UserTypeEnum),nullable=False)
    is_active = Column(Boolean, default=True)

    customer_booking = relationship(
        "Bookings",
        foreign_keys="Bookings.customer_id",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    provider_booking = relationship(
        "Bookings",
        foreign_keys="Bookings.provider_id",
        back_populates="provider"
    )


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer,  primary_key=True, index=True)
    name = Column(String(50),nullable=False)
    description = Column(String(50), nullable=True)
    price = Column(Float, nullable=False)
    duration_minutes = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    service_booking = relationship(
        "Bookings",
        foreign_keys="Bookings.service_id",
        back_populates="service"
    )

class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer,  primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer,  ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer,  ForeignKey("services.id"), nullable=False)
    booking_date = Column(DateTime(timezone=True))
    status = Column(SQLAlchemyEnum(BookingStatusEnum), nullable=False)

    customer = relationship(
        "Users",
        foreign_keys=[customer_id],
        back_populates="customer_booking"
    )
    provider = relationship(
        "Users",
        foreign_keys=[provider_id],
        back_populates="provider_booking"
    )

    service = relationship(
        "Services",
        foreign_keys=[service_id],
        back_populates="service_booking"
    )