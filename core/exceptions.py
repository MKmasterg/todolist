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
