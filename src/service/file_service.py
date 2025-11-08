import uuid

from config import MAX_FILE_SIZE_MB
from src.repository.file_repository import FileRepository
from src.repository.model.file import File
from src.service.supabase_storage_service import SupabaseStorageService


class FileService:
    def __init__(self, file_repo: FileRepository, storage_service: SupabaseStorageService):
        self.file_repo = file_repo
        self.storage_service = storage_service

    async def upload_file(self, user_id: int, filename: str, file_data: bytes) -> File:
        file_size = len(file_data)
        max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

        if file_size > max_size_bytes:
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB")

        unique_filename = f"{uuid.uuid4()}_{filename}"
        url = await self.storage_service.upload_file(unique_filename, file_data)
        return await self.file_repo.create_file(user_id, filename, url, file_size)

    async def get_file(self, file_id: int) -> File | None:
        return await self.file_repo.get_file_by_id(file_id)

    async def get_files(
        self, limit: int = 10, offset: int = 0, sort_by: str = "upload_timestamp", order: str = "desc"
    ) -> tuple[list[File], int]:
        file_list = await self.file_repo.get_files(limit, offset, sort_by, order)
        total_count = await self.file_repo.get_files_count()
        return file_list, total_count

    async def download_file(self, file_id: int) -> tuple[bytes, str] | None:
        file = await self.file_repo.get_file_by_id(file_id)
        if not file:
            return None

        storage_path = file.url.split("/")[-1]
        file_data = await self.storage_service.download_file(storage_path)
        return file_data, file.filename

    async def update_filename(self, file_id: int, new_filename: str) -> File | None:
        return await self.file_repo.update_filename(file_id, new_filename)

    async def delete_file(self, file_id: int) -> bool:
        file = await self.file_repo.get_file_by_id(file_id)
        if not file:
            return False

        storage_path = file.url.split("/")[-1]
        await self.storage_service.delete_file(storage_path)
        return await self.file_repo.delete_file(file_id)
