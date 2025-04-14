from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from upload_service.domain.models import FileMetadata


class FileMetadataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_metadata(self, metadata: dict):
        db_obj = FileMetadata(**metadata)
        self.session.add(db_obj)
        await self.session.commit()

    async def get_metadata(self, file_id: str) -> FileMetadata:
        metadata = await self.session.get(FileMetadata, file_id)
        if not metadata:
            raise HTTPException(status_code=404, detail="File metadata not found")
        return metadata
