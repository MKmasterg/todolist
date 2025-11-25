from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Project
from data.repositories.project_repository import ProjectRepository
from core.validators.project_validators import (
    validate_project_name,
    validate_project_description
)
from core.exceptions import ProjectNotFoundError


async def get_project_from_name(db: AsyncSession, name: str) -> Optional[Project]:
    validate_project_name(name)
    repo = ProjectRepository(db)
    project_model = await repo.get_by_name(name)
    if not project_model:
        return None
    project = Project(name=project_model.name, description=project_model.description or "")
    return project


async def create_project(db: AsyncSession, name: str, desc: str) -> bool:
    validate_project_name(name)
    validate_project_description(desc)
    repo = ProjectRepository(db)
    await repo.create_project(name, desc)
    await db.commit()
    return True


async def update_project(db: AsyncSession, old_name: str, updated_project: Project) -> bool:
    validate_project_name(old_name)
    validate_project_name(updated_project.get_name())
    validate_project_description(updated_project.get_description())
    repo = ProjectRepository(db)
    await repo.update_project(old_name, updated_project.get_name(), updated_project.get_description())
    await db.commit()
    return True


async def delete_project(db: AsyncSession, project: Project) -> bool:
    validate_project_name(project.get_name())
    repo = ProjectRepository(db)
    await repo.delete_project(project.get_name())
    await db.commit()
    return True


async def get_project_list(db: AsyncSession) -> List[Project]:
    repo = ProjectRepository(db)
    project_models = await repo.get_all_projects()
    projects = []
    for pm in project_models:
        project = Project(name=pm.name, description=pm.description or "")
        projects.append(project)
    return projects
