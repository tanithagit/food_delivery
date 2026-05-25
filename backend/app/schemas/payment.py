from pydantic import BaseModel

class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str
    amount: float
    currency: str

class PaymentConfirm(BaseModel):
    payment_intent_id: str