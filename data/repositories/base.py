from abc import ABC
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base repository with common async CRUD operations"""

    def __init__(self, db: AsyncSession, model_class):
        """Initialize the repository with an async database session and model class.
        :param db: The async database session.
        :param model_class: The SQLAlchemy model class for this repository.
        """
        self.db: AsyncSession = db
        self.model_class = model_class

    async def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve an entity by its ID asynchronously.
        :param id: The ID of the entity to retrieve.
        :return: The entity if found, None otherwise.
        """
        result = await self.db.execute(select(self.model_class).where(self.model_class.id == id))
        return result.scalars().first()

    async def get_all(self) -> List[T]:
        """Retrieve all entities asynchronously.
        :return: List of all entities.
        """
        result = await self.db.execute(select(self.model_class))
        return result.scalars().all()

    async def add(self, entity: T) -> T:
        """Add a new entity to the database asynchronously.
        :param entity: The entity to add.
        :return: The added entity.
        """
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def update(self, entity: T) -> T:
        """Update an existing entity in the database asynchronously.
        :param entity: The entity to update.
        :return: The updated entity.
        """
        merged = await self.db.merge(entity)
        await self.db.flush()
        return merged

    async def delete(self, entity: T) -> None:
        """Delete an entity from the database asynchronously.
        :param entity: The entity to delete.
        """
        await self.db.delete(entity)
        await self.db.flush()