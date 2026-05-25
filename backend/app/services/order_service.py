from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.cart import Cart, CartItem
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant

VALID_STATUS_TRANSITIONS = {
    "pending": ["confirmed", "canceled"],
    "confirmed": ["preparing", "canceled"],
    "preparing": ["out_for_delivery"],
    "out_for_delivery": ["delivered"],
    "delivered": [],
    "canceled": []
}

def validate_cart_and_get_total(db: Session, user_id: int) -> tuple:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty"
        )

    total = 0.0
    restaurant_id = None
    validated_items = []

    for cart_item in cart.items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == cart_item.menu_item_id
        ).first()

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item {cart_item.menu_item_id} not found"
            )

        if not menu_item.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item '{menu_item.name}' is no longer available"
            )

        if restaurant_id is None:
            restaurant_id = menu_item.restaurant_id
        elif restaurant_id != menu_item.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart contains items from multiple restaurants"
            )

        subtotal = menu_item.price * cart_item.quantity
        total += subtotal
        validated_items.append({
            "menu_item_id": menu_item.id,
            "quantity": cart_item.quantity,
            "price": menu_item.price,
            "item_name": menu_item.name
        })

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id,
        Restaurant.is_active == True
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant is not available"
        )

    return cart, restaurant_id, total, validated_items


def create_order_after_payment(
    db: Session,
    user_id: int,
    restaurant_id: int,
    total_amount: float,
    validated_items: list,
    stripe_payment_intent_id: str
) -> Order:
    from app.models.payment import Payment

    order = Order(
        user_id=user_id,
        restaurant_id=restaurant_id,
        total_amount=total_amount,
        status=OrderStatus.pending,
        payment_status=PaymentStatus.paid
    )
    db.add(order)
    db.flush()

    for item in validated_items:
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item["menu_item_id"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(order_item)

    payment = Payment(
        order_id=order.id,
        stripe_payment_intent_id=stripe_payment_intent_id,
        status="paid",
        amount=total_amount
    )
    db.add(payment)
    db.commit()
    db.refresh(order)
    return order


def clear_cart_after_order(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart:
        for item in cart.items:
            db.delete(item)
        db.commit()


def get_order_response(db: Session, order: Order) -> dict:
    items = []
    for order_item in order.items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == order_item.menu_item_id
        ).first()
        items.append({
            "id": order_item.id,
            "menu_item_id": order_item.menu_item_id,
            "quantity": order_item.quantity,
            "price": order_item.price,
            "item_name": menu_item.name if menu_item else "Unknown"
        })
    return {
        "id": order.id,
        "user_id": order.user_id,
        "restaurant_id": order.restaurant_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "items": items
    }


def get_customer_orders(db: Session, user_id: int) -> list:
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return [get_order_response(db, order) for order in orders]


def get_restaurant_orders(db: Session, owner_id: int) -> list:
    restaurant = db.query(Restaurant).filter(
        Restaurant.owner_id == owner_id
    ).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have a restaurant"
        )
    orders = db.query(Order).filter(
        Order.restaurant_id == restaurant.id
    ).all()
    return [get_order_response(db, order) for order in orders]


def update_order_status(db: Session, order_id: int, new_status: str, owner_id: int) -> dict:
    restaurant = db.query(Restaurant).filter(
        Restaurant.owner_id == owner_id
    ).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have a restaurant"
        )
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.restaurant_id == restaurant.id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    allowed = VALID_STATUS_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot move from '{order.status}' to '{new_status}'. Allowed: {allowed}"
        )
    order.status = new_status
    db.commit()
    db.refresh(order)
    return get_order_response(db, order)