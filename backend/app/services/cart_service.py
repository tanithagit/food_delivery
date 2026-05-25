from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cart import Cart, CartItem
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.schemas.cart import AddToCart, UpdateCartItem

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def build_cart_response(db: Session, cart: Cart) -> dict:
    items = []
    total = 0.0
    for cart_item in cart.items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == cart_item.menu_item_id
        ).first()
        subtotal = menu_item.price * cart_item.quantity
        total += subtotal
        items.append({
            "id": cart_item.id,
            "menu_item_id": cart_item.menu_item_id,
            "quantity": cart_item.quantity,
            "item_name": menu_item.name,
            "item_price": menu_item.price,
            "subtotal": subtotal
        })
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": items,
        "total": total
    }

def add_item_to_cart(db: Session, user_id: int, data: AddToCart) -> dict:
    menu_item = db.query(MenuItem).filter(MenuItem.id == data.menu_item_id).first()
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    if not menu_item.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This menu item is not available"
        )
    if data.quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be at least 1"
        )

    cart = get_or_create_cart(db, user_id)

    # Check if cart already has items from a different restaurant
    if cart.items:
        existing_item = cart.items[0]
        existing_menu_item = db.query(MenuItem).filter(
            MenuItem.id == existing_item.menu_item_id
        ).first()
        if existing_menu_item.restaurant_id != menu_item.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can only order from one restaurant at a time. Clear your cart first."
            )

    # If item already in cart, increase quantity
    existing_cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.menu_item_id == data.menu_item_id
    ).first()

    if existing_cart_item:
        existing_cart_item.quantity += data.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            menu_item_id=data.menu_item_id,
            quantity=data.quantity
        )
        db.add(new_item)

    db.commit()
    db.refresh(cart)
    return build_cart_response(db, cart)

def get_cart(db: Session, user_id: int) -> dict:
    cart = get_or_create_cart(db, user_id)
    return build_cart_response(db, cart)

def update_cart_item(db: Session, user_id: int, cart_item_id: int, data: UpdateCartItem) -> dict:
    cart = get_or_create_cart(db, user_id)
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart.id
    ).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    if data.quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be at least 1"
        )
    cart_item.quantity = data.quantity
    db.commit()
    db.refresh(cart)
    return build_cart_response(db, cart)

def remove_cart_item(db: Session, user_id: int, cart_item_id: int) -> dict:
    cart = get_or_create_cart(db, user_id)
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart.id
    ).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return build_cart_response(db, cart)

def clear_cart(db: Session, user_id: int) -> dict:
    cart = get_or_create_cart(db, user_id)
    for item in cart.items:
        db.delete(item)
    db.commit()
    db.refresh(cart)
    return build_cart_response(db, cart)