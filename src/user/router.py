from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_helper import get_async_session
from src.user.schemas import UserReadSchemas, UserUpdateSchemas, UserCreateSchemas
from src.user.service import UserService
router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[UserReadSchemas], summary="Список всех пользователей")
async def get_all_users(db:AsyncSession = Depends(get_async_session)):
    return await UserService.get_all_user(db)


@router.get("/{user_id}", response_model=UserReadSchemas, summary="Получить пользователя по id")
async def get_by_id_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        return await UserService.get_by_id_user(db, user_id)
    except ValueError as exc:
        if str(exc) == str(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@router.delete("/{user_id}", response_model=UserReadSchemas, summary="Удалить пользователя по id")
async def delete_by_id_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        return await UserService.delete_by_id_user(db, user_id)
    except ValueError as exc:
        if str(exc) == str(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")