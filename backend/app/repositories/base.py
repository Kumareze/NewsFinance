from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Base Repository class implementing standard CRUD interface.
    Separates database SQL mechanics from business service layers.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: any) -> Optional[ModelType]:
        """Fetch a single record by primary key."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Fetch multiple paginated records."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj: ModelType) -> ModelType:
        """Create a new database record and commit the transaction."""
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, *, id: any) -> Optional[ModelType]:
        """Delete a record by primary key."""
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
