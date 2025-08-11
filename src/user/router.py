from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db_helper import get_async_session
from src.user.schemas import UserCreate, UserRead
from src.user.service import UserService
from src.utils.security import decode_jwt

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserRead, status_code=201)
async def register(dto: UserCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        return await UserService.register(db, dto)
    except ValueError as e:
        if str(e) == "email_taken":
            raise HTTPException(409, "Email already registered")
        raise

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_async_session)):
    try:
        access, refresh = await UserService.authenticate(db, email, password)
        return {"access": access, "refresh": refresh}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_jwt(token)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(401, "Invalid token")

@router.get("/me", response_model=UserRead)
async def me(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session),
):
    try:
        return await UserService.get(db, user_id)
    except ValueError:
        raise HTTPException(404, "Not found")
