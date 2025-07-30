# src/product/models.py
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.base import Base  # ваш общий DeclarativeBase

class Product(Base):
    __tablename__ = "products"

    # 2) Основные поля
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(1024))

    # 3) Цена — Numeric (10 цифр всего, 2 после запятой)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # 4) Внешние ключи
    seller_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    # 5) Отношения (необязательно, но удобно)
    seller: Mapped["User"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")
