"""Exceptions shared across the dis-api-clients package."""


class APIError(Exception):
    """Base API error raised when an API request fails."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
