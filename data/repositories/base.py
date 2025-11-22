from abc import ABC
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, db: Session, model_class):
        self.db = db
        self.model_class = model_class

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model_class).all()

    def add(self, entity: T) -> T:
        self.db.add(entity)
        self.db.flush()
        return entity

    def update(self, entity: T) -> T:
        self.db.merge(entity)
        self.db.flush()
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(entity)
        self.db.flush()