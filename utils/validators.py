from core.exceptions import *

from datetime import datetime


def validate_project_name(name: str) -> bool:
    """Validate the project name to ensure it meets specific criteria.
    :param name: The project name to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if not (30 >= len(name.split()) and len(name) > 0):
        raise InvalidProjectNameSizeError("Project name must be at most 30 characters and not empty.")

    return True


def validate_project_description(description: str) -> bool:
    """Validate the project description to ensure it meets specific criteria.
    :param description: The project description to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if description and not (len(description.split()) <= 150 and len(description) > 0):
        raise InvalidProjectDescriptionSizeError("Project description must be at most 150 characters and not empty.")

    return True


def validate_task_title(title: str) -> bool:
    """Validate the task title to ensure it meets specific criteria.
    :param title: The task title to validate.
    :return: True if valid, raise an exception if invalid.
    """
    word_count = len(title.split())
    if not (30 >= word_count > 0):
        raise InvalidTaskTitleSizeError("Task title must be at most 30 words and not empty.")

    return True


def validate_task_description(description: str) -> bool:
    """Validate the task description to ensure it meets specific criteria.
    :param description: The task description to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if description:
        word_count = len(description.split())
        if not (0 < word_count <= 150):
            raise InvalidTaskDescriptionSizeError("Task description must be at most 150 words and not empty.")

    return True


def validate_task_status(status: str) -> bool:
    """Validate the task status to ensure it is one of the allowed values.
    :param status: The task status to validate.
    :return: True if valid, raise an exception if invalid.
    """
    valid_statuses = ['todo', 'doing', 'done']
    if status not in valid_statuses:
        raise InvalidTaskStatusError(f"Task status must be one of: {', '.join(valid_statuses)}.")

    return True


def validate_task_deadline(deadline: datetime | str) -> bool:
    """Validate the task deadline to ensure it is a valid date.
    :param deadline: The task deadline to validate (can be string, datetime, or None).
    :return: True if valid, raise an exception if invalid.
    """
    if deadline is None:
        return True

    now = datetime.now()
    # If it's already a datetime object, it's valid
    if isinstance(deadline, datetime):
        if deadline < now:
            raise InvalidTaskDeadlineError("Task deadline must be a future date.")
        return True

    # If it's a string, try to parse it
    if isinstance(deadline, str):
        try:
            date = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
            if date < now:
                raise InvalidTaskDeadlineError("Task deadline must be a future date.")
            return True
        except ValueError:
            raise InvalidTaskDeadlineError("Task deadline must be a valid date format (ISO 8601).")

    raise InvalidTaskDeadlineError("Task deadline must be a valid date.")
