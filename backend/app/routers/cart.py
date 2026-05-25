from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_customer
from app.models.user import User
from app.schemas.cart import AddToCart, UpdateCartItem, CartResponse
from app.services.cart_service import (
    add_item_to_cart, get_cart,
    update_cart_item, remove_cart_item, clear_cart
)

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartResponse)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return get_cart(db, current_user.id)

@router.post("/", response_model=CartResponse)
def add_to_cart(
    data: AddToCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return add_item_to_cart(db, current_user.id, data)

@router.put("/{cart_item_id}", response_model=CartResponse)
def update_item(
    cart_item_id: int,
    data: UpdateCartItem,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return update_cart_item(db, current_user.id, cart_item_id, data)

@router.delete("/{cart_item_id}", response_model=CartResponse)
def remove_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return remove_cart_item(db, current_user.id, cart_item_id)

@router.delete("/", response_model=CartResponse)
def clear_my_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return clear_cart(db, current_user.id)