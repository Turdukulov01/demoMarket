from typing import Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User

class UserRepository:
    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[User]:
        res = await db.execute(select(User))
        return res.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        res = await db.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        res = await db.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, **data) -> User:
        obj = User(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @staticmethod
    async def delete_by_id(db: AsyncSession, user_id: int) -> bool:
        res = await db.execute(delete(User).where(User.id == user_id))
        await db.commit()
        return res.rowcount > 0
