from fastapi import Depends

from src.dependencies.repository import get_file_repository, get_user_repository
from src.repository.file_repository import FileRepository
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService
from src.service.file_service import FileService
from src.service.supabase_storage_service import SupabaseStorageService


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)


def get_storage_service() -> SupabaseStorageService:
    return SupabaseStorageService()


def get_file_service(
    file_repo: FileRepository = Depends(get_file_repository),
    storage_service: SupabaseStorageService = Depends(get_storage_service),
) -> FileService:
    return FileService(file_repo, storage_service)
