import uuid
from io import BytesIO

from fastapi import UploadFile

from upload_service.adapters.minio_client import MinioClient
from upload_service.adapters.repository import FileMetadataRepository
from upload_service.domain.dto import FileUploadResponse


class UploadService:
    def __init__(self, minio_client: MinioClient, repo: FileMetadataRepository):
        self.minio_client = minio_client
        self.repo = repo

    async def upload_file(self, file: UploadFile) -> FileUploadResponse:
        file_id = str(uuid.uuid4())
        minio_url = await self.minio_client.upload_file(file, file_id)
        metadata = {
            "file_id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": file.size,
            "minio_url": minio_url
        }
        await self.repo.save_metadata(metadata)
        return FileUploadResponse(**metadata)

    async def get_file_metadata(self, file_id: str) -> FileUploadResponse:
        metadata = await self.repo.get_metadata(file_id)
        return FileUploadResponse(
            file_id=metadata.file_id,
            filename=metadata.filename,
            content_type=metadata.content_type,
            file_size=metadata.file_size,
            minio_url=metadata.minio_url
        )

    async def get_file(self, file_id: str) -> BytesIO:
        return await self.minio_client.get_file(file_id)
