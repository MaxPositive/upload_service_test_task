from enum import Enum

from fastapi import UploadFile, HTTPException
from pydantic import BaseModel, field_validator


class AllowedFileTypes(Enum):
    DICOM = "application/dicom"
    JPEG = "image/jpeg"
    PNG = "image/png"
    PDF = "application/pdf"


class FileUploadRequest(BaseModel):
    file: UploadFile

    @field_validator("file")
    def validate_content_type(cls, v):
        allowed = {member.value for member in AllowedFileTypes}
        if v.content_type not in allowed:
            raise HTTPException(
                status_code=422,
                detail="Unsupported file type=" + v.content_type + ". Allowed types: " + ", ".join(allowed)
            )
        return v


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    content_type: str
    file_size: int
    minio_url: str
