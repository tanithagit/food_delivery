from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_customer, get_current_restaurant_owner
from app.models.user import User
from app.schemas.order import OrderResponse, OrderStatusUpdate
from app.schemas.payment import PaymentIntentResponse, PaymentConfirm
from app.services.order_service import (
    validate_cart_and_get_total,
    create_order_after_payment,
    clear_cart_after_order,
    get_customer_orders,
    get_restaurant_orders,
    update_order_status,
    get_order_response
)
from app.services.payment_service import create_payment_intent, verify_payment_intent
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

# Step 1: Customer initiates checkout — validates cart and creates payment intent
@router.post("/checkout", response_model=PaymentIntentResponse)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    cart, restaurant_id, total, validated_items = validate_cart_and_get_total(
        db, current_user.id
    )
    payment_data = create_payment_intent(total)
    # Store validated data temporarily in payment metadata
    import stripe
    from app.core.config import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.PaymentIntent.modify(
        payment_data["payment_intent_id"],
        metadata={
            "user_id": str(current_user.id),
            "restaurant_id": str(restaurant_id),
            "total": str(total),
        }
    )
    return payment_data


# Step 2: Customer confirms payment — order is created only if payment succeeded
@router.post("/confirm", response_model=OrderResponse)
def confirm_order(
    data: PaymentConfirm,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    payment_success = verify_payment_intent(data.payment_intent_id)
    if not payment_success:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment not completed. Please complete payment first."
        )

    cart, restaurant_id, total, validated_items = validate_cart_and_get_total(
        db, current_user.id
    )

    order = create_order_after_payment(
        db=db,
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        total_amount=total,
        validated_items=validated_items,
        stripe_payment_intent_id=data.payment_intent_id
    )

    clear_cart_after_order(db, current_user.id)

    return get_order_response(db, order)


# Customer views their orders
@router.get("/my-orders", response_model=List[OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return get_customer_orders(db, current_user.id)


# Restaurant owner views incoming orders
@router.get("/restaurant-orders", response_model=List[OrderResponse])
def restaurant_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return get_restaurant_orders(db, current_user.id)


# Restaurant owner updates order status
@router.put("/{order_id}/status", response_model=OrderResponse)
def update_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return update_order_status(db, order_id, data.status, current_user.id)