from io import BytesIO
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from upload_service.di.upload_service import get_upload_service
from upload_service.entrypoints.fastapi_app import get_fastapi_app, add_routers
from upload_service.services.upload_service import UploadService
from upload_service.adapters.minio_client import MinioClient
from upload_service.adapters.repository import FileMetadataRepository


@pytest.fixture
def app():
    app = get_fastapi_app()
    add_routers(app)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def mock_minio_client(mocker):
    minio_client = MagicMock(spec=MinioClient)
    minio_client.upload_file = AsyncMock(
        return_value="http://minio:9000/uploads/test-file-id"
    )
    minio_client.get_file = AsyncMock(return_value=BytesIO(b"test file content"))
    return minio_client


@pytest.fixture
def mock_repository(mocker):
    repository = MagicMock(spec=FileMetadataRepository)
    repository.save_metadata = AsyncMock()
    repository.get_metadata = AsyncMock(
        return_value=MagicMock(
            file_id="test-file-id",
            filename="test.jpg",
            content_type="image/jpeg",
            file_size=1234,
            minio_url="http://minio:9000/uploads/test-file-id"
        )
    )
    return repository


@pytest.fixture
def mock_upload_service(mock_minio_client, mock_repository):
    upload_service = MagicMock(spec=UploadService)
    upload_service.upload_file = AsyncMock()
    upload_service.get_file_metadata = AsyncMock()
    upload_service.get_file = AsyncMock()
    return upload_service


@pytest.fixture(autouse=True)
def override_get_upload_service(mock_upload_service, app):
    app.dependency_overrides[get_upload_service] = lambda: mock_upload_service