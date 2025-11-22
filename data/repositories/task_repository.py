from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from data.models import TaskModel
from data.repositories.base import BaseRepository
from core.exceptions import TaskNotFoundError, ProjectNotFoundError


class TaskRepository(BaseRepository[TaskModel]):
    def __init__(self, db: Session):
        """Initialize the task repository.
        :param db: The database session.
        """
        super().__init__(db, TaskModel)

    def get_by_uuid(self, uuid: str) -> Optional[TaskModel]:
        """Get task by UUID.
        :param uuid: The UUID of the task to retrieve.
        :return: The TaskModel if found, None otherwise.
        """
        return self.db.query(TaskModel).filter(TaskModel.uuid == uuid).first()

    def get_tasks_by_project(self, project_id: int) -> List[TaskModel]:
        """Get all tasks for a project.
        :param project_id: The ID of the project.
        :return: List of all TaskModel instances for the given project.
        """
        return self.db.query(TaskModel).filter(TaskModel.project_id == project_id).all()

    def create_task(self, project_id: int, title: str, description: str = "",
                   status: str = "todo", deadline: Optional[datetime] = None) -> TaskModel:
        """Create a new task.
        :param project_id: The ID of the project to add the task to.
        :param title: The title of the task.
        :param description: The description of the task (optional).
        :param status: The status of the task (default: "todo").
        :param deadline: The deadline for the task (optional).
        :return: The created TaskModel.
        """
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
        """Update task details.
        :param uuid: The UUID of the task to update.
        :param title: The new title for the task.
        :param description: The new description for the task.
        :param status: The new status for the task.
        :param deadline: The new deadline for the task.
        :return: The updated TaskModel.
        """
        task = self.get_by_uuid(uuid)
        if not task:
            raise TaskNotFoundError(f"Task with uuid '{uuid}' not found.")

        setattr(task, 'title', title)
        setattr(task, 'description', description)
        setattr(task, 'status', status)
        setattr(task, 'deadline', deadline)
        return self.update(task)

    def delete_task(self, uuid: str) -> None:
        """Delete task by UUID.
        :param uuid: The UUID of the task to delete.
        """
        task = self.get_by_uuid(uuid)
        if not task:
            raise TaskNotFoundError(f"Task with uuid '{uuid}' not found.")
        self.delete(task)