class UserAlreadyExistsError(Exception):
    """Exception raised when a user already exists in the system."""

    pass


class UserNotFoundError(Exception):
    """Exception raised when a user is not found in the system."""

    pass


class DataCorruptionError(Exception):
    """Exception raised when data corruption is detected."""

    pass
