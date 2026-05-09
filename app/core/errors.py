class AppError(Exception):
    """Base application error."""


class ConflictError(AppError):
    """Raised when object already exists."""


class UnauthorizedError(AppError):
    """Raised when authentication failed."""


class ForbiddenError(AppError):
    """Raised when user has no access."""


class NotFoundError(AppError):
    """Raised when object was not found."""


class ExternalServiceError(AppError):
    """Raised when external service failed."""
