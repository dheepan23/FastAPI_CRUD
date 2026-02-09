from fastapi import FastAPI
from database.database import engine,Base
from app.routers.users import router
from database.models import Users
app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(router)