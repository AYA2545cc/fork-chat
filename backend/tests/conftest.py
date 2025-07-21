"""
Test configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.models import Conversation, Message, AttachedFile


@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database session.
    """
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()


@pytest.fixture
def sample_conversation(test_db):
    """
    Create a sample conversation for testing.
    """
    conversation = Conversation(title="Test Conversation")
    test_db.add(conversation)
    test_db.commit()
    test_db.refresh(conversation)
    return conversation


@pytest.fixture
def sample_message(test_db, sample_conversation):
    """
    Create a sample message for testing.
    """
    message = Message(
        conversation_id=sample_conversation.id,
        role="user",
        content="Test message content",
        node_summary="Test summary"
    )
    test_db.add(message)
    test_db.commit()
    test_db.refresh(message)
    return message