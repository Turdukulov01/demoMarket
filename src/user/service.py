from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.security import hash_password, verify_password, issue_tokens, decode_jwt
from src.user.repository import UserRepository
from src.user.schemas import UserCreate, UserRead

class UserService:
    @staticmethod
    async def list(db: AsyncSession) -> list[UserRead]:
        objs = await UserRepository.list_all(db)
        return [UserRead.model_validate(o) for o in objs]

    @staticmethod
    async def get(db: AsyncSession, user_id: int) -> UserRead:
        obj = await UserRepository.get_by_id(db, user_id)
        if not obj: raise ValueError("user_not_found")
        return UserRead.model_validate(obj)

    @staticmethod
    async def register(db: AsyncSession, dto: UserCreate) -> UserRead:
        if await UserRepository.get_by_email(db, dto.email):
            raise ValueError("email_taken")
        user = await UserRepository.create(
            db,
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            phone_number=dto.phone_number,
            password_hash=hash_password(dto.password),
        )
        return UserRead.model_validate(user)

    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> tuple[str, str]:
        user = await UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("bad_credentials")
        return issue_tokens(str(user.id))

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> None:
        ok = await UserRepository.delete_by_id(db, user_id)
        if not ok: raise ValueError("user_not_found")
