from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.model.file import File


class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_file(self, user_id: int, filename: str, url: str, size: int) -> File:
        file = File(user_id=user_id, filename=filename, url=url, size=size)
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def get_file_by_id(self, file_id: int, user_id: int | None = None) -> File | None:
        query = select(File).filter(File.id == file_id)
        if user_id is not None:
            query = query.filter(File.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_files(
        self,
        user_id: int,
        limit: int = 10,
        offset: int = 0,
        sort_by: str = "upload_timestamp",
        order: str = "desc",
    ) -> list[File]:
        sort_column = getattr(File, sort_by, File.upload_timestamp)
        query = select(File).filter(File.user_id == user_id)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        query = query.limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_files_count(self, user_id: int) -> int:
        query = select(func.count()).select_from(File).filter(File.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def update_filename(self, file_id: int, new_filename: str, user_id: int) -> File | None:
        file = await self.get_file_by_id(file_id, user_id)
        if not file:
            return None
        file.filename = new_filename
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def delete_file(self, file_id: int, user_id: int) -> bool:
        result = await self.db.execute(delete(File).filter(File.id == file_id, File.user_id == user_id))
        await self.db.commit()
        return result.rowcount > 0
