"""
Created by shqtes on 03.06.2026.
"""
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from core.security import hash_password, verify_password, create_access_token
import schemas.user as user_schemas
import models.user as user_models

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        user_data: user_schemas.UserRegister,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(user_models.User).where(user_models.User.email == user_data.email))

    user = result.scalars().one_or_none()

    if not user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user = user_models.User(
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.post("/login", response_model=user_schemas.TokenResponse, status_code=status.HTTP_200_OK)
async def login(
        user_data: user_schemas.UserLogin,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(user_models.User).where(user_models.User.email == user_data.email))

    user = result.scalars().one_or_none()

    if user is None or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(user.user_id)

    return {"access_token": token, "token_type": "bearer"}
