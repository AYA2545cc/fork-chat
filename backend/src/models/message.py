"""
Message model for storing chat messages with branching support.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base


class Message(Base):
    """
    Model for storing chat messages with tree structure support.
    
    Attributes:
        id: Primary key
        conversation_id: Foreign key to conversation
        parent_message_id: Foreign key to parent message (for branching)
        role: Message role ('user' or 'model')
        content: Message content
        node_summary: Summary for tree view display
        created_at: Creation timestamp
        conversation: Related conversation
        parent_message: Parent message (for branching)
        child_messages: Child messages (branches)
        attached_files: Related file attachments
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    parent_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    node_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Add constraint for role values
    __table_args__ = (
        CheckConstraint("role IN ('user', 'model')", name="check_role"),
    )

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    parent_message = relationship("Message", remote_side=[id], back_populates="child_messages")
    child_messages = relationship("Message", back_populates="parent_message", cascade="all, delete-orphan")
    attached_files = relationship("AttachedFile", back_populates="message", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', content='{self.content[:50]}...')>"