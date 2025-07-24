# schemas/product.py
from pydantic import BaseModel, ConfigDict, PositiveInt, PositiveFloat, constr

class ProductBase(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: constr(max_length=1024) | None = None
    price: PositiveFloat  # или Decimal
    seller_id: PositiveInt
    category_id: PositiveInt

class ProductCreate(ProductBase):
    """DTO для POST /products — создаёт новый товар."""
    # ничего добавлять не нужно

class ProductRead(ProductBase):
    """DTO для отдачи товара клиенту."""
    id: int
    model_config = ConfigDict(from_attributes=True)  # ← читаем из ORM

class ProductUpdate(ProductBase):
    id: int

