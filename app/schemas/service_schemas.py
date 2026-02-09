from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    duration_minutes: float


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True