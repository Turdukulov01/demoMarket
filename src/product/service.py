# src/product/service.py
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.product.repository import ProductRepo
from src.product.schemas import ProductCreate, ProductUpdate, ProductRead

class ProductService:
    """Бизнес-операции с товарами."""

    # 1) Получить все товары
    @staticmethod
    async def list_products(
            db: AsyncSession
    ) -> Sequence[ProductRead]:
        raw_items = await ProductRepo.list_all(db)
        return [ProductRead.from_orm(obj) for obj in raw_items]

    # 2) Один товар по id
    @staticmethod
    async def get_product(
            db: AsyncSession,
            product_id: int
    ) -> ProductRead:
        obj = await ProductRepo.get_by_id(db, product_id)
        if obj is None:
            # Сервис решает условие, а не роутер
            raise ValueError("product_not_found")
        return ProductRead.from_orm(obj)

    # 3) Создание
    @staticmethod
    async def create_product(
            db: AsyncSession,
            dto: ProductCreate
    ) -> ProductRead:
        # ➜ бизнес-правило: цена ≥ 0
        if dto.price < 0:
            raise ValueError("invalid_price")
        obj = await ProductRepo.create(db, dto.model_dump())
        return ProductRead.from_orm(obj)

    # 4) Обновление (PATCH/PUT)
    @staticmethod
    async def update_product(
        db: AsyncSession,
        product_id: int,
        dto: ProductUpdate
    ) -> ProductRead:
        if dto.price is not None and dto.price < 0:
            raise ValueError("invalid_price")
        obj = await ProductRepo.update(db, product_id, dto.model_dump())
        if obj is None:
            raise ValueError("product_not_found")
        return ProductRead.from_orm(obj)

    # 5) Удаление
    @staticmethod
    async def delete_product(
            db: AsyncSession,
            product_id: int
    ) -> None:
        await ProductRepo.delete(db, product_id)
