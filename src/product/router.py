# src/product/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_helper import get_async_session
from src.product.schemas import ProductCreateDTO, ProductUpdateDTO, ProductReadDTO
from src.product.service import ProductService

router = APIRouter(
    prefix="/products",         # все адреса начинаются с /products
    tags=["Products"]           # группа в Swagger UI
)

# ---------- READ (list) ----------
@router.get("/", response_model=list[ProductReadDTO], summary="Список всех товаров")
async def list_products(db: AsyncSession = Depends(get_async_session)):
    return await ProductService.list_products(db)

# ---------- READ (single) ----------
@router.get("/{product_id}", response_model=ProductReadDTO, summary="Получить товар по ID")
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        return await ProductService.get_product(db, product_id)
    except ValueError as exc:
        if str(exc) == "product_not_found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

# ---------- CREATE ----------
@router.post(
    "/",
    response_model=ProductReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый товар"
)
async def create_product(dto: ProductCreateDTO, db: AsyncSession = Depends(get_async_session)):
    try:
        return await ProductService.create_product(db, dto)
    except ValueError as exc:
        if str(exc) == "invalid_price":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Price must be ≥ 0")

# ---------- UPDATE ----------
@router.put("/{product_id}", response_model=ProductReadDTO, summary="Обновить товар целиком")
async def update_product(
    product_id: int,
    dto: ProductUpdateDTO,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await ProductService.update_product(db, product_id, dto)
    except ValueError as exc:
        match str(exc):
            case "product_not_found":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            case "invalid_price":
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Price must be ≥ 0")

# ---------- DELETE ----------
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить товар")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    await ProductService.delete_product(db, product_id)
