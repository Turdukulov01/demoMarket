from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.repository import UserRepository
from src.user.schemas import UserSchemas

class UserService:
    """Бизнес операции с user"""

    # 1. получить всех юзеров
    @staticmethod
    async def get_all_user(db: AsyncSession) -> Sequence[UserSchemas]:
        all_users = await UserRepository.list_all_user(db)
        return [UserSchemas.from_orm(obj) for obj in all_users]


    @staticmethod
    async def get_by_id_user(db: AsyncSession, id_user: int) -> UserSchemas:
        user = await UserRepository.get_by_id_user(db, id_user)
        return UserSchemas.from_orm(user)


    @staticmethod
    async def delete_by_id_user(db: AsyncSession, id_user: int) -> None:
            await UserRepository.delete_user_by_id(db, id_user)