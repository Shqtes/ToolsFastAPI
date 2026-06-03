"""
Created by shqtes on 03.06.2026.
"""
from pydantic import Field, ConfigDict, BaseModel, EmailStr
from decimal import Decimal

base_config = ConfigDict(from_attributes=True)  # Чтобы


class ToolBase(BaseModel):
    name: str = Field(..., max_length=25)
    description: str | None = Field(default=None, max_length=255)
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class ToolCreate(ToolBase):
    pass


class ToolResponse(ToolBase):
    tool_id: int

    model_config = base_config


class ToolUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=25)  # None если поле необязательно, ... если поле обязательно
    description: str | None = Field(default=None, max_length=255)
    price: Decimal | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)

    model_config = base_config
