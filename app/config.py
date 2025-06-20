from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env
load_dotenv(verbose=True)


class Settings(BaseSettings):
    APP_PORT: int = 8080
    # Database
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str


settings = Settings()
