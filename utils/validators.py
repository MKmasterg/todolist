from core.exceptions import *

from core.services import is_project_name_existing


def validate_project_name(name: str) -> bool:
    """Validate the project name to ensure it meets specific criteria.
    :param name: The project name to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if not (30 <= len(name) <= 150):
        raise InvalidProjectNameSizeError("Project name must be between 30 and 150 characters.")

    # Check if the name is duplicated
    if is_project_name_existing(name):
        raise DuplicateProjectNameError(f"Project name '{name}' already exists.")

    return True


def validate_project_description(description: str) -> bool:
    """Validate the project description to ensure it meets specific criteria.
    :param description: The project description to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if description and not (30 <= len(description) <= 150):
        raise InvalidProjectDescriptionSizeError("Project description must be between 30 and 150 characters.")

    return True
