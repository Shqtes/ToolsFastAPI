"""
Created by shqtes on 03.06.2026.
"""
from fastapi import HTTPException, status, Depends, Query, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from core.security import get_current_user
import schemas.tool as tool_schemas
import models.user as user_models
import models.tool as tool_models

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("/", response_model=list[tool_schemas.ToolResponse], status_code=status.HTTP_200_OK)
async def get_tools(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        session: AsyncSession = Depends(get_session),
        current_user: user_models.User = Depends(get_current_user),
):
    result = await session.execute(select(tool_models.Tool).offset(skip).limit(limit))

    return result.scalars().all()


@router.get("/{tool_id}", response_model=tool_schemas.ToolResponse, status_code=status.HTTP_200_OK)
async def get_tool(
        tool_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: user_models.User = Depends(get_current_user),
):
    tool = await session.get(tool_models.Tool, tool_id)

    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")

    return tool


@router.post("/", response_model=tool_schemas.ToolResponse, status_code=status.HTTP_201_CREATED)
async def create_tool(
        tool_data: tool_schemas.ToolCreate,
        session: AsyncSession = Depends(get_session),
        current_user: user_models.User = Depends(get_current_user),
):
    tool_data_obj = tool_models.Tool(**tool_data.model_dump())  # Распаковка значений словаря в атрибуты объекта.

    session.add(tool_data_obj)
    await session.commit()  # После завершения транзакции объект tool очищается из памяти, поэтому либо нужен refresh, либо expire_on_commit=False
    await session.refresh(tool_data_obj)

    return tool_data_obj


@router.patch("/{tool_id}", response_model=tool_schemas.ToolResponse, status_code=status.HTTP_200_OK)
async def update_tool(
        tool_id: int,
        tool_data: tool_schemas.ToolUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: user_models.User = Depends(get_current_user),
):
    tool = await session.get(tool_models.Tool, tool_id)

    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")

    update_dict = tool_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(tool, key, value)

    # После завершения транзакции объект tool очищается из памяти,
    # поэтому либо нужен refresh, либо expire_on_commit=False
    await session.commit()
    await session.refresh(tool)

    return tool


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(
        tool_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: user_models.User = Depends(get_current_user),
):
    tool = await session.get(tool_models.Tool, tool_id)

    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")

    await session.delete(tool)
    await session.commit()

    return
