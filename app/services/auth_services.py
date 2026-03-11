from sqlalchemy.orm import Session
from database.models import Users
from app.utils.security import verify_password
from app.utils.jwt_handler import create_access_token

def login_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise ValueError("Invalid email")
    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")
    token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }