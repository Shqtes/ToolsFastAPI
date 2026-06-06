"""
Created by shqtes on 06.06.2026.
"""
from fastapi import status, Depends, APIRouter
from core.security import get_current_user
import schemas.user as user_schemas
import models.user as user_models

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=user_schemas.UserInfoResponse, status_code=status.HTTP_200_OK)
async def get_user_info(
        current_user: user_models.User = Depends(get_current_user)
):
    return {"id": current_user.user_id, "email": current_user.email}
