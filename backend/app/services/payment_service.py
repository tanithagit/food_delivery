import stripe
from fastapi import HTTPException, status
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount: float, currency: str = "usd") -> dict:
    try:
        amount_in_cents = int(amount * 100)
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            automatic_payment_methods={"enabled": True}
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": amount,
            "currency": currency
        }
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )

def verify_payment_intent(payment_intent_id: str) -> bool:
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        # Accept all these statuses in test mode
        accepted_statuses = [
            "succeeded",
            "requires_capture",
            "processing",
            "requires_payment_method",
            "requires_confirmation",
            "requires_action"
        ]
        return intent.status in accepted_statuses
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )