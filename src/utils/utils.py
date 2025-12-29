"""
Utility functions for the Moodim application.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Type


class Utils:
    """Utility class with helper methods."""

    @staticmethod
    def get_datetime_utc_now() -> datetime:
        """Get current UTC datetime."""
        return datetime.now(timezone.utc)

    @staticmethod
    def format_date(date: datetime) -> str:
        """Format datetime to ISO format string."""
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse date string to datetime."""
        return datetime.strptime(date_str, "%Y-%m-%d")

    @staticmethod
    def get_fastapi_exception_responses(
        exceptions: List[Type[Exception]],
    ) -> Dict[int, Dict[str, Any]]:
        """
        Generate FastAPI exception responses for documentation.

        Args:
            exceptions: List of exception classes.

        Returns:
            Dictionary of status codes to response schemas.
        """
        responses = {}
        for exc in exceptions:
            if hasattr(exc, "status_code"):
                status_code = getattr(exc, "status_code")
                responses[status_code] = {
                    "description": exc.__name__,
                    "content": {
                        "application/json": {"example": {"detail": exc.__name__}}
                    },
                }
        return responses
