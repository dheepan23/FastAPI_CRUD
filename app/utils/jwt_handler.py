from jose import jwt,JWTError
from datetime import timedelta,datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Users
import os
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=10
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(data :dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    print('enjw',encoded_jwt)

    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme),db : Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(Users).filter(Users.id == int(user_id)).first()
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user