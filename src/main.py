# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.base import Base
from src.utils.db_helper import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: создаём таблицы, если их ещё нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown: можно закрыть пул, если хотите (не обязательно для SQLite)

app = FastAPI(
    title="FastAPI Marketplace",
    lifespan=lifespan
)

# подключаем роутеры как обычно
from src.product.router import router as product_router
from src.user.router import router as user_router
from src.category.router import router as category_router
app.include_router(product_router)
app.include_router(user_router)
app.include_router(category_router)

