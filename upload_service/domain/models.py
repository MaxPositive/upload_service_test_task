import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FileMetadata(Base):
    __tablename__ = "file_metadata"
    file_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    minio_url = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
        nullable=False
    )
