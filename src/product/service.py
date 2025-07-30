# src/product/service.py
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.product.repository import ProductRepository
from src.product.schemas import ProductCreateDTO, ProductUpdateDTO, ProductReadDTO

class ProductService:
    """Бизнес-операции с товарами."""

    # 1) Получить все товары
    @staticmethod
    async def list_products(
            db: AsyncSession
    ) -> Sequence[ProductReadDTO]:
        raw_items = await ProductRepository.list_all_item(db)
        return [ProductReadDTO.from_orm(obj) for obj in raw_items]

    # 2) Один товар по id
    @staticmethod
    async def get_product(
            db: AsyncSession,
            product_id: int
    ) -> ProductReadDTO:
        obj = await ProductRepository.get_by_id_item(db, product_id)
        if obj is None:
            # Сервис решает условие, а не роутер
            raise ValueError("product_not_found")
        return ProductReadDTO.from_orm(obj)

    # 3) Создание
    @staticmethod
    async def create_product(
            db: AsyncSession,
            dto: ProductCreateDTO
    ) -> ProductReadDTO:
        # ➜ бизнес-правило: цена ≥ 0
        if dto.price < 0:
            raise ValueError("invalid_price")
        obj = await ProductRepository.create_item(db, dto.model_dump())
        return ProductReadDTO.from_orm(obj)

    # 4) Обновление (PATCH/PUT)
    @staticmethod
    async def update_product_id(
        db: AsyncSession,
        product_id: int,
        dto: ProductUpdateDTO
    ) -> ProductReadDTO:
        if dto.price is not None and dto.price < 0:
            raise ValueError("invalid_price")
        obj = await ProductRepository.update_item_id(db, product_id, dto.model_dump())
        if obj is None:
            raise ValueError("product_not_found")
        return ProductReadDTO.from_orm(obj)

    # 5) Удаление
    @staticmethod
    async def delete_product_id(
            db: AsyncSession,
            product_id: int
    ) -> None:
        await ProductRepository.delete_item_id(db, product_id)
