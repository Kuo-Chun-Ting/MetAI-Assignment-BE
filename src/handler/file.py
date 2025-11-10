from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from src.dependencies.auth import get_current_user
from src.dependencies.service import get_file_service
from src.handler.schema.file import FileListResponse, FileResponse, UpdateFilenameRequest
from src.repository.model.user import User
from src.service.file_service import FileService


file_router = APIRouter(prefix="/files", tags=["files"])


@file_router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
) -> FileResponse:
    file_data = await file.read()
    uploaded_file = await service.upload_file(current_user.id, file.filename, file_data)
    return FileResponse.model_validate(uploaded_file)


@file_router.get("", response_model=FileListResponse)
async def get_files(
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "upload_timestamp",
    order: str = "desc",
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
) -> FileListResponse:
    file_list, total_count = await service.get_files(current_user.id, limit, offset, sort_by, order)
    return FileListResponse(
        file_list=[FileResponse.model_validate(f) for f in file_list],
        total=total_count,
        limit=limit,
        offset=offset,
    )


@file_router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
) -> FileResponse:
    file = await service.get_file(current_user.id, file_id)
    return FileResponse.model_validate(file)


@file_router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
):
    file_data, filename = await service.download_file(current_user.id, file_id)
    return StreamingResponse(
        iter([file_data]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@file_router.put("/{file_id}", response_model=FileResponse)
async def update_filename(
    file_id: int,
    request: UpdateFilenameRequest,
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
) -> FileResponse:
    file = await service.update_filename(current_user.id, file_id, request.filename)
    return FileResponse.model_validate(file)


@file_router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
):
    await service.delete_file(current_user.id, file_id)
    return {"message": "File deleted successfully"}
