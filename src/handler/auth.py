from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.auth import get_current_user
from src.dependencies.service import get_auth_service
from src.handler.schema.auth import AuthResponse, LoginRequest, RegisterRequest
from src.repository.model.user import User
from src.service.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    try:
        user = await service.register(request.username, request.password)
        token = service.create_access_token(user)
        return AuthResponse(username=user.username, token=token, message="User registered successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)) -> AuthResponse:
    try:
        user = await service.verify_credentials(request.username, request.password)
        token = service.create_access_token(user)
        return AuthResponse(username=user.username, token=token, message="Login successful")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user), service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    service.invalidate_user_tokens(current_user.id)
    return {"message": "Logout successful"}
