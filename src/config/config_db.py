from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = "sqlite:///./test.db"
    db_echo: bool = True
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30

settings = Settings()