from pydantic import BaseModel
from datetime import datetime

class RestaurantCreate(BaseModel):
    name: str
    description: str = None
    address: str = None

class RestaurantUpdate(BaseModel):
    name: str = None
    description: str = None
    address: str = None
    is_active: bool = None

class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: str = None
    address: str = None
    owner_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True