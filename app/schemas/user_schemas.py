from pydantic import BaseModel, EmailStr
from database.db_enum import UserTypeEnum
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserTypeEnum


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None
    is_active : Optional[bool] = None

    class Config:
        from_attributes = True