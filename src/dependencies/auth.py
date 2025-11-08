from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dependencies.service import get_auth_service
from src.repository.model.user import User
from src.service.auth_service import AuthService

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing bearer token")

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = credentials.credentials
    try:
        return await service.get_user_from_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
