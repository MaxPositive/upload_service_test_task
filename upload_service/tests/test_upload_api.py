from io import BytesIO

import pytest
from fastapi import HTTPException

from upload_service.domain.dto import FileUploadResponse, AllowedFileTypes


@pytest.mark.asyncio
class TestUploadAPI:
    async def test_upload_file_success(self, client, mock_upload_service):
        file_content = b"test image content"
        file_name = "test.jpg"
        mock_upload_service.upload_file.return_value = FileUploadResponse(
            file_id="test-file-id",
            filename=file_name,
            content_type="image/jpeg",
            file_size=len(file_content),
            minio_url="http://minio:9000/uploads/test-file-id"
        )

        response = client.post(
            "/upload/",
            files={"file": (file_name, file_content, "image/jpeg")}
        )

        assert response.status_code == 201
        json_response = response.json()
        assert json_response["file_id"] == "test-file-id"
        assert json_response["filename"] == file_name
        assert json_response["content_type"] == "image/jpeg"
        assert json_response["file_size"] == len(file_content)
        assert json_response["minio_url"] == "http://minio:9000/uploads/test-file-id"
        mock_upload_service.upload_file.assert_called_once()

    async def test_upload_file_unsupported_type(self, client, mock_upload_service):
        response = client.post(
            "/upload/",
            files={"file": ("test.txt", b"test content", "text/plain")}
        )
        allowed = {member.value for member in AllowedFileTypes}

        assert response.status_code == 422
        message = "Unsupported file type=" + "text/plain" + ". Allowed types: " + ", ".join(allowed)
        assert response.json() == {"detail": message}
        assert not mock_upload_service.upload_file.called

    async def test_get_file_metadata_success(self, client, mock_upload_service):
        file_id = "test-file-id"
        mock_upload_service.get_file_metadata.return_value = FileUploadResponse(
            file_id=file_id,
            filename="test.jpg",
            content_type="image/jpeg",
            file_size=1234,
            minio_url="http://minio:9000/uploads/test-file-id"
        )

        response = client.get(f"/upload/{file_id}")

        assert response.status_code == 200
        json_response = response.json()
        assert json_response["file_id"] == file_id
        assert json_response["filename"] == "test.jpg"
        assert json_response["content_type"] == "image/jpeg"
        assert json_response["file_size"] == 1234
        assert json_response["minio_url"] == "http://minio:9000/uploads/test-file-id"
        mock_upload_service.get_file_metadata.assert_called_once_with(file_id)

    async def test_get_file_metadata_not_found(self, client, mock_upload_service):
        file_id = "non-existent-id"
        mock_upload_service.get_file_metadata.side_effect = HTTPException(
            status_code=404, detail="File metadata not found"
        )

        response = client.get(f"/upload/{file_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "File metadata not found"}
        mock_upload_service.get_file_metadata.assert_called_once_with(file_id)

    async def test_download_file_success(self, client, mock_upload_service):
        file_id = "test-file-id"
        file_content = b"test file content"
        mock_upload_service.get_file.return_value = BytesIO(file_content)
        mock_upload_service.get_file_metadata.return_value = FileUploadResponse(
            file_id=file_id,
            filename="test.jpg",
            content_type="image/jpeg",
            file_size=len(file_content),
            minio_url="http://minio:9000/uploads/test-file-id"
        )

        response = client.get(f"/upload/{file_id}/download")

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"
        assert response.headers["content-disposition"] == "attachment; filename=test.jpg"
        assert response.content == file_content
        mock_upload_service.get_file.assert_called_once_with(file_id)
        mock_upload_service.get_file_metadata.assert_called_once_with(file_id)

    async def test_download_file_not_found(self, client, mock_upload_service):
        file_id = "non-existent-id"
        mock_upload_service.get_file.side_effect = HTTPException(
            status_code=404, detail="File not found in MinIO"
        )
        mock_upload_service.get_file_metadata.side_effect = HTTPException(
            status_code=404, detail="File metadata not found"
        )

        response = client.get(f"/upload/{file_id}/download")

        assert response.status_code == 404
        assert response.json() == {"detail": "File metadata not found"}
        mock_upload_service.get_file_metadata.assert_called_once_with(file_id)