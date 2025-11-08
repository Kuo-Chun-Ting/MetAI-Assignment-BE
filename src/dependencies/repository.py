from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.repository.file_repository import FileRepository
from src.repository.user_repository import UserRepository


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_file_repository(db: AsyncSession = Depends(get_db)) -> FileRepository:
    return FileRepository(db)
