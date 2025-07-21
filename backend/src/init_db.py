"""
Database initialization script.
"""
import os
from sqlalchemy import create_engine
from .database import Base, DATABASE_URL
from .models import Conversation, Message, AttachedFile


def init_database():
    """
    Initialize the database by creating all tables.
    """
    print(f"Initializing database at: {DATABASE_URL}")
    
    # Ensure data directory exists
    if "sqlite" in DATABASE_URL:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create engine
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database()