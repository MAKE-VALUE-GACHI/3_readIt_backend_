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
    # OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    # JWT
    SECRET_KEY: str
    # OpenAI
    OPENAI_API_KEY: str


settings = Settings()
