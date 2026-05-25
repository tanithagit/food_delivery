import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="tanitha1309@gmail.com",
    MAIL_PASSWORD="reakwtawntbqfuqr",
    MAIL_FROM="tanitha1309@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def test():
    message = MessageSchema(
        subject="Test Email from FoodDelivery",
        recipients=["tanitha1309@gmail.com"],
        body="<h2>Email is working! ✅</h2><p>Your food delivery email notifications are configured correctly.</p>",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    print("Email sent successfully ✅")

asyncio.run(test())