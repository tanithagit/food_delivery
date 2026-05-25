from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_customer, get_current_restaurant_owner
from app.models.user import User
from app.models.user import User as UserModel
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
from app.services.email_service import send_order_confirmation_email, send_status_update_email
from typing import List
import asyncio

router = APIRouter(prefix="/orders", tags=["Orders"])


def run_email(coro):
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(coro)
        loop.close()
    except Exception as e:
        print(f"Email error: {e}")


@router.post("/checkout", response_model=PaymentIntentResponse)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    cart, restaurant_id, total, validated_items = validate_cart_and_get_total(
        db, current_user.id
    )
    payment_data = create_payment_intent(total)
    return payment_data


@router.post("/confirm", response_model=OrderResponse)
def confirm_order(
    data: PaymentConfirm,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    from fastapi import HTTPException, status

    payment_success = verify_payment_intent(data.payment_intent_id)
    if not payment_success:
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

    # Send confirmation email
    import threading
    threading.Thread(
        target=run_email,
        args=(send_order_confirmation_email(
            email=current_user.email,
            order_id=order.id,
            total=order.total_amount
        ),)
    ).start()

    return get_order_response(db, order)


@router.get("/my-orders", response_model=List[OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    return get_customer_orders(db, current_user.id)


@router.get("/restaurant-orders", response_model=List[OrderResponse])
def restaurant_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    return get_restaurant_orders(db, current_user.id)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_restaurant_owner)
):
    order_data = update_order_status(db, order_id, data.status, current_user.id)

    # Get customer email and send status update email
    customer = db.query(UserModel).filter(
        UserModel.id == order_data["user_id"]
    ).first()

    if customer:
        import threading
        threading.Thread(
            target=run_email,
            args=(send_status_update_email(
                email=customer.email,
                order_id=order_id,
                new_status=data.status
            ),)
        ).start()

    return order_data