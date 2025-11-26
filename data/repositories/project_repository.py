from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from data.models import ProjectModel
from data.repositories.base import BaseRepository
from core.exceptions import ProjectNotFoundError, DuplicateProjectNameError


class ProjectRepository(BaseRepository[ProjectModel]):
    def __init__(self, db: AsyncSession):
        """Initialize the project repository.
        :param db: The async database session.
        """
        super().__init__(db, ProjectModel)

    async def get_by_name(self, name: str) -> Optional[ProjectModel]:
        """Get project by name asynchronously."""
        result = await self.db.execute(select(ProjectModel).where(ProjectModel.name == name))
        return result.scalars().first()

    async def exists_by_name(self, name: str) -> bool:
        """Check if project with given name exists asynchronously."""
        result = await self.db.execute(select(func.count()).select_from(ProjectModel).where(ProjectModel.name == name))
        count = result.scalar_one()
        return count > 0

    async def create_project(self, name: str, description: str = "") -> ProjectModel:
        """Create a new project asynchronously."""
        if await self.exists_by_name(name):
            raise DuplicateProjectNameError(f"Project with name '{name}' already exists.")

        project = ProjectModel(name=name, description=description)
        return await self.add(project)

    async def update_project(self, old_name: str, new_name: str, new_description: str) -> ProjectModel:
        """Update project details asynchronously."""
        project = await self.get_by_name(old_name)
        if not project:
            raise ProjectNotFoundError(f"Project with name '{old_name}' not found.")

        if new_name != old_name and await self.exists_by_name(new_name):
            raise DuplicateProjectNameError(f"Project with name '{new_name}' already exists.")

        setattr(project, 'name', new_name)
        setattr(project, 'description', new_description)
        return await self.update(project)

    async def delete_project(self, name: str) -> None:
        """Delete project by name asynchronously."""
        project = await self.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project with name '{name}' not found.")
        await self.delete(project)

    async def get_all_projects(self) -> List[ProjectModel]:
        """Get all projects asynchronously."""
        return await self.get_all()