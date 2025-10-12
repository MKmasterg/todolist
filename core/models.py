from utils.validators import validate_project_name, validate_project_description, validate_task_title, \
    validate_task_description, validate_task_status, validate_task_deadline

from core.exceptions import MaxProjectsReachedError, MaxTasksReachedError

from data.env_loader import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK

from datetime import datetime

from typing import Optional

import uuid


class Status:
    """Enumeration for task statuses."""
    TODO = 'todo'
    DOING = 'doing'
    DONE = 'done'


class Task:
    """Represents a task with title, description, status, and deadline."""
    task_count = 0

    def __init__(self, title: str, description: str = "", status: str = Status.TODO, deadline: Optional[datetime] = None):
        """
        Initialize a new Task instance.

        :param title: Task title (max 30 words)
        :param description: Task description (max 150 words)
        :param status: Task status (todo, doing, or done) - defaults to 'todo'
        :param deadline: Optional task deadline
        """
        if Task.task_count >= MAX_NUMBER_OF_TASK:
            raise MaxTasksReachedError(
                f"Cannot create more tasks. Maximum limit of {MAX_NUMBER_OF_TASK} reached.")

        # Validate all fields
        is_title_valid = validate_task_title(title)
        is_desc_valid = validate_task_description(description)
        is_status_valid = validate_task_status(status)
        is_deadline_valid = validate_task_deadline(deadline)

        if is_title_valid and is_desc_valid and is_status_valid and is_deadline_valid:
            self.uuid = str(uuid.uuid4())
            self.title = title
            self.description = description
            self.status = status
            self.deadline = deadline
            Task.task_count += 1

    def set_status(self, new_status: str):
        """
        Update the task status.

        :param new_status: New status (must be one of: todo, doing, done)
        """
        if validate_task_status(new_status):
            self.status = new_status

    def set_deadline(self, new_deadline: Optional[datetime]):
        """
        Update the task deadline.

        :param new_deadline: New deadline (must be a valid date or None)
        """
        if validate_task_deadline(new_deadline):
            self.deadline = new_deadline


class Project:
    project_count = 0

    def __init__(self, name: str, description: str = ""):
        if Project.project_count >= MAX_NUMBER_OF_PROJECT:
            raise MaxProjectsReachedError(
                f"Cannot create more projects. Maximum limit of {MAX_NUMBER_OF_PROJECT} reached.")

        is_name_valid = validate_project_name(name)
        is_desc_valid = validate_project_description(description)
        if is_name_valid and is_desc_valid:
            self.name = name
            self.description = description
            Project.project_count += 1
