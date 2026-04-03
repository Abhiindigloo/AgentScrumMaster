from typing import Any


class AppException(Exception):
    """Base exception for all application-level errors.

    Attributes:
        message:     Human-readable error description.
        status_code: HTTP status code to return to the caller.
        details:     Optional structured error details.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Any = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ValidationError(AppException):
    """Raised when request data fails domain-level validation."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            message=message,
            status_code=422,
            details=details,
        )
