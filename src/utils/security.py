from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.hash import bcrypt
from src.config.config_db import settings

def hash_password(p: str) -> str: return bcrypt.hash(p)
def verify_password(p: str, h: str) -> bool: return bcrypt.verify(p, h)

def _create_jwt(claims: dict, minutes: int) -> str:
    data = claims.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def issue_tokens(sub: str) -> tuple[str, str]:
    access = _create_jwt({"sub": sub, "typ": "access"}, settings.ACCESS_TTL_MIN)
    refresh = _create_jwt({"sub": sub, "typ": "refresh"}, settings.REFRESH_TTL_DAYS * 24 * 60)
    return access, refresh

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
