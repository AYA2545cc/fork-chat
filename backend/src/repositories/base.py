"""
Base repository class with common database operations.
"""
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository class providing common CRUD operations.
    
    Args:
        model: SQLAlchemy model class
        db: Database session
    """
    
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db
    
    def create(self, obj_in: dict) -> T:
        """
        Create a new record.
        
        Args:
            obj_in: Dictionary with object data
            
        Returns:
            Created object
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            db_obj = self.model(**obj_in)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get(self, id: int) -> Optional[T]:
        """
        Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Record if found, None otherwise
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: int, obj_in: dict) -> Optional[T]:
        """
        Update a record by ID.
        
        Args:
            id: Record ID
            obj_in: Dictionary with updated data
            
        Returns:
            Updated object if found, None otherwise
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            db_obj = self.get(id)
            if db_obj:
                for field, value in obj_in.items():
                    setattr(db_obj, field, value)
                self.db.commit()
                self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            db_obj = self.get(id)
            if db_obj:
                self.db.delete(db_obj)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e