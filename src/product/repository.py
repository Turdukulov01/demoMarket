from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.product.models import Product as ProductModel


class ProductRepository:
    """Низкоуровневые операции с таблицей products."""

    # 1. Список всех товаров
    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[ProductModel]:
        result = await db.execute(select(ProductModel))
        return result.scalars().all()                      # ↩︎ последовательность объектов ProductModel

    # 2. Получить товар по id
    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: int) -> ProductModel | None:
        result = await db.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        return result.scalar_one_or_none()                 # ↩︎ один объект или None

    # 3. Создать новый товар
    @staticmethod
    async def create(db: AsyncSession, data: dict) -> ProductModel:
        obj = ProductModel(**data)      # превращаем dict DTO → ORM
        db.add(obj)                # ставим на вставку
        await db.commit()          # подтверждаем транзакцию
        await db.refresh(obj)      # подтягиваем сгенерированный id
        return obj

    # 4. Обновить товар (PATCH/PUT)
    @staticmethod
    async def update(db: AsyncSession, product_id: int, data: dict) -> ProductModel | None:
        # удаляем ключи со значением None, чтобы оставить прежние данные
        cleaned = {k: v for k, v in data.items() if v is not None}

        await db.execute(
            update(ProductModel).where(ProductModel.id == product_id).values(**cleaned)
        )
        await db.commit()
        return await ProductRepository.get_by_id(db, product_id)

    # 5. Удалить товар
    @staticmethod
    async def delete(db: AsyncSession, product_id: int) -> None:
        await db.execute(delete(ProductModel).where(ProductModel.id == product_id))
        await db.commit()
