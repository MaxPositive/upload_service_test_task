from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Depends
from starlette.responses import StreamingResponse

from upload_service.services.upload_service import UploadService
from upload_service.domain.dto import FileUploadResponse, FileUploadRequest
from upload_service.di.upload_service import get_upload_service


router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post(
    "/",
    response_model=FileUploadResponse,
    status_code=201,
    description="Upload a file to MinIO and saving metadata to database",
    responses={
        422: {"description": "Unsupported file type"},
        201: {"description": "File uploaded successfully"}
    }
)
async def upload_file(
    file: Annotated[FileUploadRequest, File(...)],
    upload_service: Annotated[UploadService, Depends(get_upload_service)]
):
    try:
        result = await upload_service.upload_file(file.file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{file_id}",
    response_model=FileUploadResponse,
    status_code=200,
    description="Get file metadata from database",
    responses={
        404: {"description": "File metadata not found"},
        200: {"description": "File metadata found"}
    }
)
async def get_file_metadata(
    file_id: str,
    upload_service: Annotated[UploadService, Depends(get_upload_service)]
):
    return await upload_service.get_file_metadata(file_id)


@router.get(
    "/{file_id}/download",
    status_code=200,
    description="Download file from MinIO",
    responses={
        404: {
            "description":
                "File not found: either metadata is missing in the database or the file is not present in MinIO"
        },
        200: {"description": "File found in MinIO"}
    }
)
async def download_file(
    file_id: str,
    upload_service: Annotated[UploadService, Depends(get_upload_service)]
):
    metadata = await upload_service.get_file_metadata(file_id)
    file_stream = await upload_service.get_file(file_id)
    return StreamingResponse(
        file_stream,
        media_type=metadata.content_type,
        headers={"Content-Disposition": f"attachment; filename={metadata.filename}"}
    )