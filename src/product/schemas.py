# schemas/product.py
from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt, PositiveFloat, constr

class ProductBaseDTO(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: constr(max_length=1024) | None = None
    price: PositiveFloat  # или Decimal
    seller_id: PositiveInt
    category_id: PositiveInt
    created: datetime
    updated_at: datetime
    is_active: bool

class ProductCreateDTO(ProductBaseDTO):
    """DTO для POST /products — создаёт новый товар."""
    # ничего добавлять не нужно

class ProductReadDTO(ProductBaseDTO):
    """DTO для отдачи товара клиенту."""
    id: int
    model_config = ConfigDict(from_attributes=True)  # ← читаем из ORM

class ProductUpdateDTO(ProductBaseDTO):
    id: int

