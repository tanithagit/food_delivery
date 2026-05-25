from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate

# ─── Restaurant ───────────────────────────────────────────

def create_restaurant(db: Session, data: RestaurantCreate, owner_id: int) -> Restaurant:
    existing = db.query(Restaurant).filter(
        Restaurant.owner_id == owner_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a restaurant"
        )
    restaurant = Restaurant(
        name=data.name,
        description=data.description,
        address=data.address,
        owner_id=owner_id
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

def get_all_restaurants(db: Session) -> list:
    return db.query(Restaurant).filter(Restaurant.is_active == True).all()

def get_restaurant_by_id(db: Session, restaurant_id: int) -> Restaurant:
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return restaurant

def get_my_restaurant(db: Session, owner_id: int) -> Restaurant:
    restaurant = db.query(Restaurant).filter(
        Restaurant.owner_id == owner_id
    ).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have a restaurant yet"
        )
    return restaurant

def update_restaurant(db: Session, owner_id: int, data: RestaurantUpdate) -> Restaurant:
    restaurant = get_my_restaurant(db, owner_id)
    if data.name is not None:
        restaurant.name = data.name
    if data.description is not None:
        restaurant.description = data.description
    if data.address is not None:
        restaurant.address = data.address
    if data.is_active is not None:
        restaurant.is_active = data.is_active
    db.commit()
    db.refresh(restaurant)
    return restaurant

# ─── Menu Items ───────────────────────────────────────────

def create_menu_item(db: Session, restaurant_id: int, data: MenuItemCreate) -> MenuItem:
    item = MenuItem(
        restaurant_id=restaurant_id,
        name=data.name,
        description=data.description,
        price=data.price,
        is_available=data.is_available
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_menu_items(db: Session, restaurant_id: int) -> list:
    return db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id
    ).all()

def update_menu_item(db: Session, item_id: int, owner_id: int, data: MenuItemUpdate) -> MenuItem:
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == item.restaurant_id,
        Restaurant.owner_id == owner_id
    ).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this restaurant"
        )
    if data.name is not None:
        item.name = data.name
    if data.description is not None:
        item.description = data.description
    if data.price is not None:
        item.price = data.price
    if data.is_available is not None:
        item.is_available = data.is_available
    db.commit()
    db.refresh(item)
    return item

def delete_menu_item(db: Session, item_id: int, owner_id: int):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == item.restaurant_id,
        Restaurant.owner_id == owner_id
    ).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't own this restaurant"
        )
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted successfully"}