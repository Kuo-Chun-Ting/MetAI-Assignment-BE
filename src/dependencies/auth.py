from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dependencies.service import get_auth_service
from src.repository.model.user import User
from src.service.auth_service import AuthService
from src.service.error import UnauthorizedError


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    if not credentials:
        raise UnauthorizedError("Missing bearer token")

    if credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("Invalid authorization header, scheme is not 'bearer'")

    token = credentials.credentials
    return await service.get_user_from_token(token)
