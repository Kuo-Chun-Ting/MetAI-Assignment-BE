from fastapi import Depends

from src.dependencies.repository import get_user_repository
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)
