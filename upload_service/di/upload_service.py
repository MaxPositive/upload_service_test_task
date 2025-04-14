from typing import Annotated

from fastapi import Depends

from upload_service.adapters.repository import FileMetadataRepository
from upload_service.adapters.minio_client import MinioClient
from upload_service.di.minio_client import get_minio_client
from upload_service.di.repository import get_file_metadata_repository
from upload_service.services.upload_service import UploadService


def get_upload_service(
    minio_client: Annotated[MinioClient, Depends(get_minio_client)],
    repo: Annotated[FileMetadataRepository, Depends(get_file_metadata_repository)]
) -> UploadService:
    return UploadService(
        minio_client=minio_client,
        repo=repo
    )