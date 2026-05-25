from pydantic import BaseModel
from typing import List

class AddToCart(BaseModel):
    menu_item_id: int
    quantity: int = 1

class UpdateCartItem(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    item_name: str
    item_price: float
    subtotal: float

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    total: float

    class Config:
        from_attributes = True