"""
Created by shqtes on 03.06.2026.
"""
from pydantic import Field, BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=255)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
