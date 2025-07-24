# src/db/base.py  (пример)

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Абстрактный базовый класс для всех моделей."""
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)
