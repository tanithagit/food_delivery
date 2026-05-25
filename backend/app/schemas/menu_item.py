from pydantic import BaseModel
from datetime import datetime

class MenuItemCreate(BaseModel):
    name: str
    description: str = None
    price: float
    is_available: bool = True

class MenuItemUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    is_available: bool = None

class MenuItemResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str = None
    price: float
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True