from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///./test.db"
    DB_ECHO: bool = True
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    ACCESS_TTL_MIN: int = 15
    REFRESH_TTL_DAYS: int = 7


    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()

# # Эти нужны только когда перейдём на Postgres; пока можно оставить,
#      но не использовать для sqlite.
#     DB_POOL_SIZE: int = 5
#     DB_MAX_OVERFLOW: int = 10
#     DB_POOL_TIMEOUT: int = 30