from fastapi import FastAPI

from src.handler.auth import auth_router
from src.handler.file import file_router
from src.handler.health import health_router

app = FastAPI(title="MetAI File Management API")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(file_router)
