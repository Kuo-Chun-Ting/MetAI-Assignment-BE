from sqlalchemy import delete, select
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

    async def get_file_by_id(self, file_id: int) -> File | None:
        result = await self.db.execute(select(File).filter(File.id == file_id))
        return result.scalar_one_or_none()

    async def get_files(
        self, limit: int = 10, offset: int = 0, sort_by: str = "upload_timestamp", order: str = "desc"
    ) -> list[File]:
        query = select(File)
        if order == "desc":
            query = query.order_by(getattr(File, sort_by).desc())
        else:
            query = query.order_by(getattr(File, sort_by).asc())
        query = query.limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_files_count(self) -> int:
        result = await self.db.execute(select(File))
        return len(list(result.scalars().all()))

    async def update_filename(self, file_id: int, new_filename: str) -> File | None:
        file = await self.get_file_by_id(file_id)
        if not file:
            return None
        file.filename = new_filename
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def delete_file(self, file_id: int) -> bool:
        result = await self.db.execute(delete(File).filter(File.id == file_id))
        await self.db.commit()
        return result.rowcount > 0
