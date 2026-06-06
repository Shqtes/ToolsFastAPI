"""
Created by shqtes on 03.06.2026.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(url=DATABASE_URL, echo=False, pool_size=10, max_overflow=5)

# expire_on_commit=False предотвращает удаление объекта из памяти при завершении транзакции.
session_maker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_session():
    async with session_maker() as session:
        yield session
