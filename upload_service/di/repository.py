from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from upload_service.adapters.repository import FileMetadataRepository
from upload_service.di.database import get_db_session


def get_file_metadata_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> FileMetadataRepository:
    return FileMetadataRepository(
        session=session
    )
