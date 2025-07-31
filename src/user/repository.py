from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User as UserModel

class UserRepository:
    """Низкоуровневые операции с таблицей User"""

    # 1. Список юзеров
    @staticmethod
    async def list_all_user(db: AsyncSession) -> Sequence[UserModel]:
        result = await db.execute(select(UserModel))
        return result.scalars().all()

    # 2. Получить юзера по id
    @staticmethod
    async def get_by_id_user(db: AsyncSession, user_id: int) -> UserModel:
        result = await db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalars().first() # посмотреть что делает first если что поставить scalar_one_or_none()

    # 3. Delete user по Id

    @staticmethod
    async def delete_user_by_id(db: AsyncSession, user_id: int) -> None:
        await db.execute(delete(UserModel).where(UserModel.id == user_id))
        await db.commit()
