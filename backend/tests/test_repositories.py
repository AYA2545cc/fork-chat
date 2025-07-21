"""
Tests for repository classes.
"""
import pytest
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.message_repository import MessageRepository
from src.repositories.file_repository import FileRepository
from src.models import Conversation, Message, AttachedFile


class TestConversationRepository:
    """Test cases for ConversationRepository."""
    
    def test_create_conversation(self, test_db):
        """Test creating a new conversation."""
        repo = ConversationRepository(test_db)
        conversation_data = {"title": "New Conversation"}
        
        conversation = repo.create(conversation_data)
        
        assert conversation.id is not None
        assert conversation.title == "New Conversation"
        assert conversation.created_at is not None
    
    def test_get_conversation(self, test_db, sample_conversation):
        """Test getting a conversation by ID."""
        repo = ConversationRepository(test_db)
        
        retrieved = repo.get(sample_conversation.id)
        
        assert retrieved is not None
        assert retrieved.id == sample_conversation.id
        assert retrieved.title == sample_conversation.title
    
    def test_get_by_title(self, test_db, sample_conversation):
        """Test getting a conversation by title."""
        repo = ConversationRepository(test_db)
        
        retrieved = repo.get_by_title(sample_conversation.title)
        
        assert retrieved is not None
        assert retrieved.id == sample_conversation.id
    
    def test_get_recent(self, test_db):
        """Test getting recent conversations."""
        repo = ConversationRepository(test_db)
        
        # Create multiple conversations
        for i in range(3):
            repo.create({"title": f"Conversation {i}"})
        
        recent = repo.get_recent(limit=2)
        
        assert len(recent) == 2
        assert all(isinstance(conv, Conversation) for conv in recent)


class TestMessageRepository:
    """Test cases for MessageRepository."""
    
    def test_create_message(self, test_db, sample_conversation):
        """Test creating a new message."""
        repo = MessageRepository(test_db)
        message_data = {
            "conversation_id": sample_conversation.id,
            "role": "user",
            "content": "Test message",
            "node_summary": "Test summary"
        }
        
        message = repo.create(message_data)
        
        assert message.id is not None
        assert message.conversation_id == sample_conversation.id
        assert message.role == "user"
        assert message.content == "Test message"
    
    def test_get_by_conversation(self, test_db, sample_conversation, sample_message):
        """Test getting messages by conversation."""
        repo = MessageRepository(test_db)
        
        messages = repo.get_by_conversation(sample_conversation.id)
        
        assert len(messages) == 1
        assert messages[0].id == sample_message.id
    
    def test_get_root_messages(self, test_db, sample_conversation):
        """Test getting root messages."""
        repo = MessageRepository(test_db)
        
        # Create root message
        root_msg = repo.create({
            "conversation_id": sample_conversation.id,
            "role": "user",
            "content": "Root message"
        })
        
        # Create child message
        repo.create({
            "conversation_id": sample_conversation.id,
            "parent_message_id": root_msg.id,
            "role": "model",
            "content": "Child message"
        })
        
        root_messages = repo.get_root_messages(sample_conversation.id)
        
        assert len(root_messages) == 1
        assert root_messages[0].id == root_msg.id
    
    def test_get_children(self, test_db, sample_conversation):
        """Test getting child messages."""
        repo = MessageRepository(test_db)
        
        # Create parent message
        parent_msg = repo.create({
            "conversation_id": sample_conversation.id,
            "role": "user",
            "content": "Parent message"
        })
        
        # Create child message
        child_msg = repo.create({
            "conversation_id": sample_conversation.id,
            "parent_message_id": parent_msg.id,
            "role": "model",
            "content": "Child message"
        })
        
        children = repo.get_children(parent_msg.id)
        
        assert len(children) == 1
        assert children[0].id == child_msg.id


class TestFileRepository:
    """Test cases for FileRepository."""
    
    def test_create_file(self, test_db, sample_message):
        """Test creating a new file attachment."""
        repo = FileRepository(test_db)
        file_data = {
            "message_id": sample_message.id,
            "file_name": "test.pdf",
            "gemini_file_uri": "gs://test-bucket/test.pdf"
        }
        
        file_attachment = repo.create(file_data)
        
        assert file_attachment.id is not None
        assert file_attachment.message_id == sample_message.id
        assert file_attachment.file_name == "test.pdf"
        assert file_attachment.gemini_file_uri == "gs://test-bucket/test.pdf"
    
    def test_get_by_message(self, test_db, sample_message):
        """Test getting files by message."""
        repo = FileRepository(test_db)
        
        # Create file attachment
        repo.create({
            "message_id": sample_message.id,
            "file_name": "test.pdf",
            "gemini_file_uri": "gs://test-bucket/test.pdf"
        })
        
        files = repo.get_by_message(sample_message.id)
        
        assert len(files) == 1
        assert files[0].file_name == "test.pdf"