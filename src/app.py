from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.handler.auth import auth_router
from src.handler.exception import add_exception_handlers
from src.handler.file import file_router
from src.handler.health import health_router


app = FastAPI(title="MetAI File Management API")

add_exception_handlers(app)

origins = [
    "http://localhost:5173",
    "https://metai-assignment-fe.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(file_router)
