from storage3 import AsyncStorageClient
from storage3.types import FileOptions

from config import SUPABASE_ANON_KEY, SUPABASE_STORAGE_BUCKET, SUPABASE_URL


class SupabaseStorageService:
    def __init__(self):
        storage_url = f"{SUPABASE_URL}/storage/v1"
        headers = {"apiKey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}
        self.client = AsyncStorageClient(storage_url, headers)
        self.bucket = SUPABASE_STORAGE_BUCKET

    async def upload_file(self, file_path: str, file_data: bytes) -> str:
        file_options: FileOptions = {"content-type": "application/octet-stream"}
        await self.client.from_(self.bucket).upload(file_path, file_data, file_options)
        return await self.client.from_(self.bucket).get_public_url(file_path)

    async def download_file(self, file_path: str) -> bytes:
        response = await self.client.from_(self.bucket).download(file_path)
        return response

    async def delete_file(self, file_path: str) -> None:
        await self.client.from_(self.bucket).remove([file_path])
