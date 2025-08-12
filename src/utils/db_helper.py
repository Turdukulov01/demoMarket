from typing import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config.config_db import settings


"""
Создаем Асихронный движок

"""
engine = create_async_engine(
    settings.DB_URL,
    echo = settings.DB_ECHO,
    pool_size = settings.DB_POOL_SIZE,
    max_overflow = settings.DB_MAX_OVERFLOW,
    pool_timeout = settings.DB_POOL_TIMEOUT,
)


"""
Создаем фабрику асихронных сессий 

"""
async_session_local = async_sessionmaker(
    engine,
    class_= AsyncSession,
    expire_on_commit = False,
    autoflush = True,
    autocommit = False,
)

"""
Создаем асихронную сессию
"""
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local () as session:
        try:
            yield session
        finally:
            await session.close()


@event.listens_for(engine.sync_engine, "connect")
def connect(db_connection, connection_record):
    print("new connection")