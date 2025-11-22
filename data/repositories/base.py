from abc import ABC
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, db: Session, model_class):
        """Initialize the repository with a database session and model class.
        :param db: The database session.
        :param model_class: The SQLAlchemy model class for this repository.
        """
        self.db = db
        self.model_class = model_class

    def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve an entity by its ID.
        :param id: The ID of the entity to retrieve.
        :return: The entity if found, None otherwise.
        """
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    def get_all(self) -> List[T]:
        """Retrieve all entities.
        :return: List of all entities.
        """
        return self.db.query(self.model_class).all()

    def add(self, entity: T) -> T:
        """Add a new entity to the database.
        :param entity: The entity to add.
        :return: The added entity.
        """
        self.db.add(entity)
        self.db.flush()
        return entity

    def update(self, entity: T) -> T:
        """Update an existing entity in the database.
        :param entity: The entity to update.
        :return: The updated entity.
        """
        self.db.merge(entity)
        self.db.flush()
        return entity

    def delete(self, entity: T) -> None:
        """Delete an entity from the database.
        :param entity: The entity to delete.
        """
        self.db.delete(entity)
        self.db.flush()