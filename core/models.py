from core.validators.project_validators import validate_project_name, validate_project_description
from core.validators.task_validators import validate_task_title, validate_task_description, validate_task_status, validate_task_deadline

from core.exceptions import MaxProjectsReachedError, MaxTasksReachedError

from data.env_loader import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK

from datetime import datetime

from typing import Optional

from utils.id_generator import tiny_id


class Status:
    """Enumeration for task statuses."""
    TODO = 'todo'
    DOING = 'doing'
    DONE = 'done'


class Task:
    """Represents a task with title, description, status, and deadline."""

    def __init__(self, title: str, description: str = "", status: str = Status.TODO,
                 deadline: Optional[datetime | str] = None, id: Optional[int] = None, 
                 project_id: Optional[int] = None,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        """
        Initialize a new Task instance.

        :param title: Task title (max 30 words)
        :param description: Task description (max 150 words)
        :param status: Task status (todo, doing, or done) - defaults to 'todo'
        :param deadline: Optional task deadline
        :param id: Optional database ID (for internal use)
        :param project_id: Optional project ID
        :param created_at: Optional creation timestamp
        :param updated_at: Optional update timestamp
        """
        
        self.uuid = tiny_id()
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        # Extended fields for API response compatibility
        self.id = id
        self.project_id = project_id
        self.created_at = created_at
        self.updated_at = updated_at


    def get_uuid(self) -> str:
        """
        Get the task UUID.

        :return: The task UUID
        """
        return self.uuid

    def get_title(self) -> str:
        """
        Get the task title.

        :return: The task title
        """
        return self.title

    def get_description(self) -> str:
        """
        Get the task description.

        :return: The task description
        """
        return self.description

    def get_status(self) -> str:
        """
        Get the task status.

        :return: The task status
        """
        return self.status

    def get_deadline(self) -> Optional[datetime | str]:
        """
        Get the task deadline.

        :return: The task deadline
        """
        return self.deadline

    def set_title(self, new_title: str):
        """
        Update the task title.

        :param new_title: New task title (must be between 30 and 150 words)
        """
        self.title = new_title

    def set_description(self, new_description: str):
        """
        Update the task description.

        :param new_description: New task description (must be between 30 and 150 words)
        """
        self.description = new_description

    def set_status(self, new_status: str):
        """
        Update the task status.

        :param new_status: New status (must be one of: todo, doing, done)
        """
        if validate_task_status(new_status):
            self.status = new_status

    def set_deadline(self, new_deadline: datetime | str):
        """
        Update the task deadline.

        :param new_deadline: New deadline (must be a valid date or None)
        """
        self.deadline = new_deadline


class Project:

    def __init__(self, name: str, description: str = "", id: Optional[int] = None,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.name = name
        self.description = description
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    def get_name(self) -> str:
        """
        Get the project name.

        :return: The project name
        """
        return self.name

    def get_description(self) -> str:
        """
        Get the project description.

        :return: The project description
        """
        return self.description

    def set_name(self, new_name: str):
        """
        Update the project name.

        :param new_name: New project name (must be between 30 and 150 characters)
        """

        self.name = new_name

    def set_description(self, new_description: str):
        """
        Update the project description.

        :param new_description: New project description (must be between 30 and 150 characters)
        """
        
        self.description = new_description
