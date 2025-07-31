from src.base import Base
from pydantic import EmailStr
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=False
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=False
    )
    email: Mapped[EmailStr] = mapped_column(
        String(255),
        unique=True,
        nullable=False,

    )

    phone_number: Mapped[int | str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="seller",
        cascade="all, delete-orphan"
    )