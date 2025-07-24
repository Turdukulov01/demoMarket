# src/category/models.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.base import Base       # ваш общий DeclarativeBase

class Category(Base):
    __tablename__ = "categories"

    # id, created, updated_at, is_active наследуются
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # обратная сторона связи к Product
    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )
