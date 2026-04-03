from typing import Any


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500, details: Any = None) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            message=f"{resource} not found: {identifier}",
            status_code=404,
        )


class ValidationError(AppException):
    """Request validation error."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(message=message, status_code=422, details=details)


class AgentError(AppException):
    """Agent processing error."""

    def __init__(self, agent_name: str, message: str) -> None:
        super().__init__(
            message=f"Agent '{agent_name}' error: {message}",
            status_code=500,
        )
