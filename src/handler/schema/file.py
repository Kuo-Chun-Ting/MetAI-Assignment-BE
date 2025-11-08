from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    id: int
    filename: str
    url: str
    size: int
    upload_timestamp: datetime

    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    file_list: list[FileResponse]
    total: int
    limit: int
    offset: int


class UpdateFilenameRequest(BaseModel):
    filename: str
