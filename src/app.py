from fastapi import FastAPI

from src.handler.health import health_router


app = FastAPI(title="MetAI File Management API")

app.include_router(health_router)
