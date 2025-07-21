"""
Repository for conversation database operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import BaseRepository
from ..models.conversation import Conversation


class ConversationRepository(BaseRepository[Conversation]):
    """
    Repository for conversation-specific database operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(Conversation, db)
    
    def get_by_title(self, title: str) -> Optional[Conversation]:
        """
        Get conversation by title.
        
        Args:
            title: Conversation title
            
        Returns:
            Conversation if found, None otherwise
        """
        return self.db.query(Conversation).filter(Conversation.title == title).first()
    
    def get_recent(self, limit: int = 10) -> List[Conversation]:
        """
        Get recent conversations ordered by updated_at.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of recent conversations
        """
        return (
            self.db.query(Conversation)
            .order_by(desc(Conversation.updated_at))
            .limit(limit)
            .all()
        )
    
    def search_by_title(self, search_term: str) -> List[Conversation]:
        """
        Search conversations by title.
        
        Args:
            search_term: Search term to match in title
            
        Returns:
            List of matching conversations
        """
        return (
            self.db.query(Conversation)
            .filter(Conversation.title.contains(search_term))
            .order_by(desc(Conversation.updated_at))
            .all()
        )
    
    def get_with_messages(self, conversation_id: int) -> Optional[Conversation]:
        """
        Get conversation with all its messages loaded.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation with messages if found, None otherwise
        """
        return (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )