"""
Created by shqtes on 03.06.2026.
"""
from fastapi import FastAPI
from api.tools import router as tools_router
from api.auth import router as auth_router
from api.users import router as users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(tools_router)
app.include_router(users_router)