import os
from pydantic_settings import BaseSettings

def str_to_bool(value: str) -> bool:
    """Convert a string to a boolean value."""
    return value.lower() in ["true", "1", "yes"] if value else False


class Settings(BaseSettings):
    BASE_URL: str = os.getenv("BASE_URL", "/api/v1/")
    # PostgreSQL configuration
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "default_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # JWT authentication settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Optional settings
    DEBUG: bool = str_to_bool(os.getenv("DEBUG", "False"))
    TESTING: bool = str_to_bool(os.getenv("TESTING", "False"))


settings = Settings()