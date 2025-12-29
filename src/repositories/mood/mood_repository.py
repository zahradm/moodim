"""
Mood repository for orchestrating mood data access.
"""

from typing import Any, Dict, List, Optional

from src.models.dtos.mood.repository.mood_repository_dtos import (
    CreateMoodCommandDTO,
    DeleteMoodCommandDTO,
    GetMoodQueryDTO,
    UpdateMoodCommandDTO,
)

from src.repositories.mood.adapters.mood_postgres_adapter import MoodPostgresAdapter


class MoodRepository:
    """
    Repository layer for mood operations.

    This repository orchestrates data access through adapters,
    providing a clean interface for the business logic layer.
    """

    def __init__(self, postgres_adapter: MoodPostgresAdapter) -> None:
        """
        Initialize the repository.

        Args:
            postgres_adapter: PostgreSQL adapter for mood operations.
        """
        self._postgres_adapter = postgres_adapter

    async def insert_mood(self, command: CreateMoodCommandDTO) -> Dict[str, Any]:
        """
        Insert a new mood entry.

        Args:
            command: Mood creation command.

        Returns:
            Created mood data.
        """
        return await self._postgres_adapter.insert_mood(command)

    async def get_moods(self, query: GetMoodQueryDTO) -> Optional[List[Dict[str, Any]]]:
        """
        Get moods for a user within a date range.

        Args:
            query: Mood query.

        Returns:
            List of mood data or None.
        """
        return await self._postgres_adapter.get_moods(query)

    async def update_mood(
        self, command: UpdateMoodCommandDTO
    ) -> Optional[Dict[str, Any]]:
        """
        Update a mood entry.

        Args:
            command: Mood update command.

        Returns:
            Updated mood data or None.
        """
        return await self._postgres_adapter.update_mood(command)

    async def delete_mood(self, command: DeleteMoodCommandDTO) -> bool:
        """
        Delete mood entries for a date.

        Args:
            command: Mood delete command.

        Returns:
            True if deleted.
        """
        return await self._postgres_adapter.delete_mood(command)
