from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_order_confirmation_email(email: str, order_id: int, total: float):
    if not settings.MAIL_USERNAME:
        print(f"Email skipped - not configured. Order {order_id} confirmed.")
        return
    message = MessageSchema(
        subject=f"Order #{order_id} Confirmed - FoodDelivery",
        recipients=[email],
        body=f"""
        <h2>Your order has been placed successfully!</h2>
        <p>Order ID: <strong>#{order_id}</strong></p>
        <p>Total Amount: <strong>${total:.2f}</strong></p>
        <p>You can track your order status in the app.</p>
        <br>
        <p>Thank you for ordering with FoodDelivery!</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_status_update_email(email: str, order_id: int, new_status: str):
    if not settings.MAIL_USERNAME:
        print(f"Email skipped - not configured. Order {order_id} status: {new_status}")
        return
    status_display = new_status.replace("_", " ").upper()
    message = MessageSchema(
        subject=f"Order #{order_id} Update - {status_display}",
        recipients=[email],
        body=f"""
        <h2>Your order status has been updated!</h2>
        <p>Order ID: <strong>#{order_id}</strong></p>
        <p>New Status: <strong>{status_display}</strong></p>
        <br>
        <p>Track your order in the FoodDelivery app.</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)