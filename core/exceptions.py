class InvalidProjectNameSizeError(Exception):
    """Custom exception for invalid project name size."""
    pass


class InvalidProjectDescriptionSizeError(Exception):
    """Custom exception for invalid project description size."""
    pass


class DuplicateProjectNameError(Exception):
    """Custom exception for duplicate project names."""
    pass


class MaxProjectsReachedError(Exception):
    """Custom exception for reaching the maximum number of projects."""
    pass


class InvalidTaskTitleSizeError(Exception):
    """Custom exception for invalid task title size."""
    pass


class InvalidTaskDescriptionSizeError(Exception):
    """Custom exception for invalid task description size."""
    pass


class InvalidTaskStatusError(Exception):
    """Custom exception for invalid task status."""
    pass


class InvalidTaskDeadlineError(Exception):
    """Custom exception for invalid task deadline."""
    pass


class MaxTasksReachedError(Exception):
    """Custom exception for reaching the maximum number of tasks."""
    pass

class ProjectNotFoundError(Exception):
    """Custom exception for when a project is not found in the database."""
    pass