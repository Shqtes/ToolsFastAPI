"""
Created by shqtes on 03.06.2026.
"""
import os
import jwt
from datetime import datetime, timedelta, UTC
from pwdlib import PasswordHash
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
import models.user as user_models

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

http_bearer = HTTPBearer(auto_error=False)  # HTTPBearer - объект содержащий тип токена и сам токен

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    # "sub" и "exp" - это зарезервированные стандартные поля, sub - subject(ID ресурса, согласно стандарту),
    # exp - expiration(дата и время истечения токена)
    payload = {
        "sub": str(user_id),  # Согласно стандарту данные в sub всегда являются строкой.
        "type": "access",  # Тип токена
        "exp": datetime.now(UTC) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.now(UTC) + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        session: AsyncSession = Depends(get_session)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token required")

    token = credentials.credentials

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_id = int(payload["sub"])
    # PyJWTError возникнет, если подпись (signature) будет подделана, или истек срок действия токена
    # PyJWTError включает исключения ExpiredSignatureError и InvalidSignatureError.
    except (jwt.PyJWTError, ValueError, KeyError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await session.get(user_models.User, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return user
