from typing import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from src.config.config_db import settings


"""
Создаем Асихронный движок

"""
engine = create_async_engine(
    settings.db_url,
    echo = settings.db_echo,
    pool_size = settings.db_pool_size,
    max_overflow = settings.db_max_overflow,
    pool_timeout = settings.db_pool_timeout,
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