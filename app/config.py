from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env
load_dotenv(verbose=True)


class Settings(BaseSettings):
    # App
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str


settings = Settings()
