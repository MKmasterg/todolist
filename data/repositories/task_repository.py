from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from data.models import TaskModel
from data.repositories.base import BaseRepository
from core.exceptions import TaskNotFoundError, ProjectNotFoundError


class TaskRepository(BaseRepository[TaskModel]):
    def __init__(self, db: Session):
        super().__init__(db, TaskModel)

    def get_by_uuid(self, uuid: str) -> Optional[TaskModel]:
        """Get task by UUID"""
        return self.db.query(TaskModel).filter(TaskModel.uuid == uuid).first()

    def get_tasks_by_project(self, project_id: int) -> List[TaskModel]:
        """Get all tasks for a project"""
        return self.db.query(TaskModel).filter(TaskModel.project_id == project_id).all()

    def create_task(self, project_id: int, title: str, description: str = "",
                   status: str = "todo", deadline: Optional[datetime] = None) -> TaskModel:
        """Create a new task"""
        task = TaskModel(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project_id
        )
        return self.add(task)

    def update_task(self, uuid: str, title: str, description: str,
                   status: str, deadline: Optional[datetime]) -> TaskModel:
        """Update task details"""
        task = self.get_by_uuid(uuid)
        if not task:
            raise TaskNotFoundError(f"Task with uuid '{uuid}' not found.")

        setattr(task, 'title', title)
        setattr(task, 'description', description)
        setattr(task, 'status', status)
        setattr(task, 'deadline', deadline)
        return self.update(task)

    def delete_task(self, uuid: str) -> None:
        """Delete task by UUID"""
        task = self.get_by_uuid(uuid)
        if not task:
            raise TaskNotFoundError(f"Task with uuid '{uuid}' not found.")
        self.delete(task)