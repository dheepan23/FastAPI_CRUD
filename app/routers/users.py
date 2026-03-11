from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database.database import get_db
from app.schemas.user_schemas import UserCreate,UserResponse,UserUpdate
from app.services.user_service import create_user,get_user_by_id,delete_user_by_id,update_user_by_id
from database.models import Users
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/create_user",response_model=UserCreate)
def create_users(user: UserCreate, db:Session=Depends(get_db)):
    try:
        return create_user(db,user)
    except HTTPException as e:
        raise e
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user",
        )
@router.get("/get_users")
def get_users(db:Session = Depends(get_db)):
    try:
        users = db.query(Users).filter(Users.is_active.is_(True))
        result =[{"id":user.id,"name":user.name,"role":user.role.value}for user in users]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result,
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the users",
        )

@router.get("/get_user",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    try:
        return get_user_by_id(db,user_id)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user",
        )
    
@router.put("/update_user",response_model=UserUpdate)
def update_user(user_id:int,user_update: UserUpdate,db:Session=Depends(get_db)):
    try:
        return update_user_by_id(db,user_id,user_update)
    except HTTPException:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user",
        )

@router.delete("/delete_user",response_model=UserResponse)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    try:
        return delete_user_by_id(db,user_id)
    except HTTPException:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )