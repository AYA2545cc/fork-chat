"""
Repository for message database operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .base import BaseRepository
from ..models.message import Message


class MessageRepository(BaseRepository[Message]):
    """
    Repository for message-specific database operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(Message, db)
    
    def get_by_conversation(self, conversation_id: int) -> List[Message]:
        """
        Get all messages for a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of messages ordered by creation time
        """
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .all()
        )
    
    def get_root_messages(self, conversation_id: int) -> List[Message]:
        """
        Get root messages (no parent) for a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of root messages
        """
        return (
            self.db.query(Message)
            .filter(
                and_(
                    Message.conversation_id == conversation_id,
                    Message.parent_message_id.is_(None)
                )
            )
            .order_by(Message.created_at)
            .all()
        )
    
    def get_children(self, parent_message_id: int) -> List[Message]:
        """
        Get child messages for a parent message.
        
        Args:
            parent_message_id: Parent message ID
            
        Returns:
            List of child messages
        """
        return (
            self.db.query(Message)
            .filter(Message.parent_message_id == parent_message_id)
            .order_by(Message.created_at)
            .all()
        )
    
    def get_conversation_thread(self, message_id: int) -> List[Message]:
        """
        Get the complete thread from root to the specified message.
        
        Args:
            message_id: Target message ID
            
        Returns:
            List of messages in the thread path
        """
        thread = []
        current_message = self.get(message_id)
        
        # Build thread by traversing up to root
        while current_message:
            thread.insert(0, current_message)
            if current_message.parent_message_id:
                current_message = self.get(current_message.parent_message_id)
            else:
                break
        
        return thread
    
    def get_by_role(self, conversation_id: int, role: str) -> List[Message]:
        """
        Get messages by role for a conversation.
        
        Args:
            conversation_id: Conversation ID
            role: Message role ('user' or 'model')
            
        Returns:
            List of messages with specified role
        """
        return (
            self.db.query(Message)
            .filter(
                and_(
                    Message.conversation_id == conversation_id,
                    Message.role == role
                )
            )
            .order_by(Message.created_at)
            .all()
        )
    
    def get_with_files(self, message_id: int) -> Optional[Message]:
        """
        Get message with attached files loaded.
        
        Args:
            message_id: Message ID
            
        Returns:
            Message with files if found, None otherwise
        """
        return (
            self.db.query(Message)
            .filter(Message.id == message_id)
            .first()
        )