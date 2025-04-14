from io import BytesIO

from minio import Minio
from fastapi import UploadFile, HTTPException

from upload_service.config import settings


class MinioClient:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False
        )
        self.bucket = settings.minio_bucket
        if not self.client.bucket_exists(settings.minio_bucket):
            self.client.make_bucket(settings.minio_bucket)

    async def upload_file(self, file: UploadFile, file_id: str) -> str:
        self.client.put_object(
            self.bucket,
            file_id,
            file.file,
            length=-1,
            part_size=10*1024*1024,
            content_type=file.content_type
        )
        return f"http://{settings.minio_endpoint}/{self.bucket}/{file_id}"

    async def get_file(self, file_id: str) -> BytesIO:
        response = None
        try:
            response = self.client.get_object(self.bucket, file_id)
            return BytesIO(response.read())
        except Exception:
            raise HTTPException(status_code=404, detail=f"File {file_id} not found in MinIO")
        finally:
            if response is not None:
                response.close()
                response.release_conn()
