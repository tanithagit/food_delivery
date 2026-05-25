from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user, get_current_restaurant_owner
from app.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services.restaurant_service import (
    create_restaurant, get_all_restaurants, get_restaurant_by_id,
    get_my_restaurant, update_restaurant, create_menu_item,
    get_menu_items, update_menu_item, delete_menu_item
)
from typing import List

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# ─── Public Routes (any logged in user) ───────────────────

@router.get("/", response_model=List[RestaurantResponse])
def list_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_restaurants(db)

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_restaurant_by_id(db, restaurant_id)

@router.get("/{restaurant_id}/menu", response_model=List[MenuItemResponse])
def get_restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_menu_items(db, restaurant_id)

# ─── Restaurant Owner Routes ──────────────────────────────

@router.post("/", response_model=RestaurantResponse)
def create_my_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return create_restaurant(db, data, current_user.id)

@router.get("/owner/me", response_model=RestaurantResponse)
def my_restaurant(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return get_my_restaurant(db, current_user.id)

@router.put("/owner/me", response_model=RestaurantResponse)
def update_my_restaurant(
    data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return update_restaurant(db, current_user.id, data)

@router.post("/owner/menu", response_model=MenuItemResponse)
def add_menu_item(
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    restaurant = get_my_restaurant(db, current_user.id)
    return create_menu_item(db, restaurant.id, data)

@router.put("/owner/menu/{item_id}", response_model=MenuItemResponse)
def update_item(
    item_id: int,
    data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return update_menu_item(db, item_id, current_user.id, data)

@router.delete("/owner/menu/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return delete_menu_item(db, item_id, current_user.id)