from typing import Optional, List
from sqlalchemy.orm import Session
from data.models import ProjectModel
from data.repositories.base import BaseRepository
from core.exceptions import ProjectNotFoundError, DuplicateProjectNameError


class ProjectRepository(BaseRepository[ProjectModel]):
    def __init__(self, db: Session):
        super().__init__(db, ProjectModel)

    def get_by_name(self, name: str) -> Optional[ProjectModel]:
        """Get project by name"""
        return self.db.query(ProjectModel).filter(ProjectModel.name == name).first()

    def exists_by_name(self, name: str) -> bool:
        """Check if project with given name exists"""
        return self.db.query(ProjectModel).filter(ProjectModel.name == name).count() > 0

    def create_project(self, name: str, description: str = "") -> ProjectModel:
        """Create a new project"""
        if self.exists_by_name(name):
            raise DuplicateProjectNameError(f"Project with name '{name}' already exists.")

        project = ProjectModel(name=name, description=description)
        return self.add(project)

    def update_project(self, old_name: str, new_name: str, new_description: str) -> ProjectModel:
        """Update project details"""
        project = self.get_by_name(old_name)
        if not project:
            raise ProjectNotFoundError(f"Project with name '{old_name}' not found.")

        if new_name != old_name and self.exists_by_name(new_name):
            raise DuplicateProjectNameError(f"Project with name '{new_name}' already exists.")

        setattr(project, 'name', new_name)
        setattr(project, 'description', new_description)
        return self.update(project)

    def delete_project(self, name: str) -> None:
        """Delete project by name"""
        project = self.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project with name '{name}' not found.")
        self.delete(project)

    def get_all_projects(self) -> List[ProjectModel]:
        """Get all projects"""
        return self.get_all()