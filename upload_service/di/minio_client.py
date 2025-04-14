from upload_service.adapters.minio_client import MinioClient


def get_minio_client() -> MinioClient:
    return MinioClient()
