"""
AttachedFile model for storing file attachment metadata.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class AttachedFile(Base):
    """
    Model for storing file attachment metadata.
    
    Attributes:
        id: Primary key
        message_id: Foreign key to message
        file_name: Original file name
        gemini_file_uri: URI from Google File API
        created_at: Creation timestamp
        message: Related message
    """
    __tablename__ = "attached_files"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    file_name = Column(String, nullable=False)
    gemini_file_uri = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    message = relationship("Message", back_populates="attached_files")

    def __repr__(self):
        return f"<AttachedFile(id={self.id}, file_name='{self.file_name}')>"