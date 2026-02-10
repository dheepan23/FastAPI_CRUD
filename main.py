from fastapi import FastAPI
from database.database import engine,Base
from app.routers import users,bookings,services
app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(services.router)