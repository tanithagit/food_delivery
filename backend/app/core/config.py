from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    APP_NAME: str = "FoodDelivery"
    DEBUG: bool = True
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"

    model_config = {"env_file": ".env"}

settings = Settings()