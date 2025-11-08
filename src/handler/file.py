from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
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
    file_list, total_count = await service.get_files(limit, offset, sort_by, order)
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
    file = await service.get_file(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse.model_validate(file)


@file_router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
):
    result = await service.download_file(file_id)
    if not result:
        raise HTTPException(status_code=404, detail="File not found")

    file_data, filename = result
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
    file = await service.update_filename(file_id, request.filename)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse.model_validate(file)


@file_router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
):
    success = await service.delete_file(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted successfully"}
