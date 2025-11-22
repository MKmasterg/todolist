from core.exceptions import *

def validate_project_name(name: str) -> bool:
    """Validate the project name to ensure it meets specific criteria.
    :param name: The project name to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if not (30 >= len(name.split()) > 0):
        raise InvalidProjectNameSizeError("Project name must be at most 30 characters and not empty.")

    return True


def validate_project_description(description: str) -> bool:
    """Validate the project description to ensure it meets specific criteria.
    :param description: The project description to validate.
    :return: True if valid, raise an exception if invalid.
    """
    if not (150 >= len(description.split())):
        raise InvalidProjectDescriptionSizeError("Project description must be at most 150 characters.")

    return True
