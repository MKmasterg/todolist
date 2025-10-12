from utils.validators import validate_project_name, validate_project_description

from core.exceptions import InvalidProjectNameSizeError, InvalidProjectDescriptionSizeError, DuplicateProjectNameError, \
    MaxProjectsReachedError

from data.env_loader import MAX_NUMBER_OF_PROJECT


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
