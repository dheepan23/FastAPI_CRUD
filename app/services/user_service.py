from database.models import Users
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate, UserUpdate
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse

def create_user(db : Session, user_create: UserCreate):
    existing_user = db.query(Users).filter(Users.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = Users(
        name=user_create.name,
        email=user_create.email,
        role=user_create.role,
        hashed_password=user_create.password
    )
    db.add(new_user)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message" : "User created successfully",
        }
    ) 

def get_user_by_id(db:Session,user_id : int):
    get_user = db.query(Users).filter(Users.id == user_id,Users.is_active.is_(True)).first()
    if not get_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="User not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message" : "User retrieved successfully",
            "data": {
                "name" : get_user.name,
                "email" : get_user.email,
                "is_active": get_user.is_active,
                "role" : get_user.role.value,
                },
        }
    )

def delete_user_by_id(db:Session,user_id : int):
    user = db.query(Users).filter(Users.id == user_id,Users.is_active.is_(True)).first()
    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

def update_user_by_id(db:Session,user_id : int,user_update: UserUpdate):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user_update.email:
        existing_email = db.query(Users.email).filter(Users.email == user_update.email,Users.id != user_id).first()
        if existing_email:
             raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
        user.email = user_update.email
    if user_update.name:
        user.name = user_update.name
    if user_update.password:
        user.hashed_password = user_update.password
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message" : "User updated successfully",
        }
    )