from typing import Optional
from core.exceptions import *

import datetime as dt_module
from datetime import datetime

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

    word_count = len(description.split())
    if not (word_count <= 150):
        raise InvalidTaskDescriptionSizeError("Task description must be at most 150 words.")

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


def validate_task_deadline(deadline: datetime | str) -> Optional[datetime]:
    """Validate the task deadline to ensure it is a valid date.
    :param deadline: The task deadline to validate (can be string, datetime, or None).
    :return: The validated datetime object, or raise an exception if invalid.
    """
    if deadline is None:
        return None

    dt_val = deadline
    if isinstance(deadline, str):
        try:
            dt_val = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        except ValueError:
            raise InvalidTaskDeadlineError("Task deadline must be a valid date format (ISO 8601).")

    if not isinstance(dt_val, datetime):
        raise InvalidTaskDeadlineError("Task deadline must be a valid date.")
    
    now = datetime.now()
    # Check if dt_val is offset-aware (has timezone info)
    if dt_val.tzinfo is not None and dt_val.tzinfo.utcoffset(dt_val) is not None:
        # If deadline is aware, we must compare against an aware 'now'
        now = datetime.now().astimezone()
    
    if dt_val < now:
        raise InvalidTaskDeadlineError("Task deadline must be a future date.")
    
    if dt_val.tzinfo is not None and dt_val.tzinfo.utcoffset(dt_val) is not None:
        # Convert to UTC and strip timezone info to make it naive
        dt_val = dt_val.astimezone(dt_module.timezone.utc).replace(tzinfo=None)
        
    return dt_val
