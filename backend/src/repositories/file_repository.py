"""
Repository for file attachment database operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.attached_file import AttachedFile


class FileRepository(BaseRepository[AttachedFile]):
    """
    Repository for file attachment-specific database operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(AttachedFile, db)
    
    def get_by_message(self, message_id: int) -> List[AttachedFile]:
        """
        Get all files attached to a message.
        
        Args:
            message_id: Message ID
            
        Returns:
            List of attached files
        """
        return (
            self.db.query(AttachedFile)
            .filter(AttachedFile.message_id == message_id)
            .order_by(AttachedFile.created_at)
            .all()
        )
    
    def get_by_filename(self, message_id: int, file_name: str) -> Optional[AttachedFile]:
        """
        Get file by message ID and filename.
        
        Args:
            message_id: Message ID
            file_name: File name
            
        Returns:
            Attached file if found, None otherwise
        """
        return (
            self.db.query(AttachedFile)
            .filter(
                AttachedFile.message_id == message_id,
                AttachedFile.file_name == file_name
            )
            .first()
        )
    
    def get_by_gemini_uri(self, gemini_file_uri: str) -> Optional[AttachedFile]:
        """
        Get file by Gemini file URI.
        
        Args:
            gemini_file_uri: Gemini file URI
            
        Returns:
            Attached file if found, None otherwise
        """
        return (
            self.db.query(AttachedFile)
            .filter(AttachedFile.gemini_file_uri == gemini_file_uri)
            .first()
        )
    
    def get_by_conversation(self, conversation_id: int) -> List[AttachedFile]:
        """
        Get all files in a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of attached files in the conversation
        """
        return (
            self.db.query(AttachedFile)
            .join(AttachedFile.message)
            .filter(AttachedFile.message.has(conversation_id=conversation_id))
            .order_by(AttachedFile.created_at)
            .all()
        )