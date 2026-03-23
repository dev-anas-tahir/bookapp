class DomainException(Exception):
    """Base exception class for domain-specific errors."""

    status_code = 400

    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class UserAlreadyExistsException(DomainException):
    """Raised when attempting to create a user that already exists."""

    status_code = 409

    def __init__(self, email: str):
        super().__init__(
            f"User with email {email} already exists", error_code="USER_EXISTS"
        )


class InvalidCredentialsException(DomainException):
    """Raised when login credentials are invalid."""

    status_code = 401

    def __init__(self):
        super().__init__("Invalid email or password", error_code="INVALID_CREDENTIALS")


class InfrastructureException(DomainException):
    """Raised when there is an infrastructure issue."""

    status_code = 500

    def __init__(self, message: str):
        super().__init__(message, error_code="INFRASTRUCTURE_ERROR")
