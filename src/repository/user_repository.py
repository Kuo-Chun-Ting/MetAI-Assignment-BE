from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.model.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def username_exists(self, username: str) -> bool:
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none() is not None

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()
