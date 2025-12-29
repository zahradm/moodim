"""
Mood business logic layer.
"""

from typing import List, Optional

from src.models.dtos.mood.domain.v1.mood_domain_dtos import (
    CreateMoodInputDTO,
    CreateMoodOutputDTO,
    GetMoodOutputDTO,
)
from src.models.dtos.mood.repository.mood_repository_dtos import (
    CreateMoodCommandDTO,
    DeleteMoodCommandDTO,
    GetMoodQueryDTO,
    UpdateMoodCommandDTO,
)
from src.repositories.mood.mood_repository import MoodRepository


class MoodLogic:
    """
    Business logic layer for mood operations.

    This class contains the business rules and orchestrates
    the flow between controllers and repositories.
    """

    def __init__(self, repository: MoodRepository) -> None:
        """
        Initialize the mood logic.

        Args:
            repository: The mood repository instance.
        """
        self._repository = repository

    async def insert_mood(self, input_dto: CreateMoodInputDTO) -> CreateMoodOutputDTO:
        """
        Insert a new mood entry.

        Args:
            input_dto: Mood data for creation.

        Returns:
            CreateMoodOutputDTO: Created mood information.
        """
        command = CreateMoodCommandDTO(
            user_id=input_dto.user_id,
            emotion=input_dto.emotion,
            percentage=input_dto.percentage,
            date=input_dto.date,
        )
        result = await self._repository.insert_mood(command)
        return CreateMoodOutputDTO(**result)

    async def get_moods(
        self,
        user_id: int,
        start_date: str,
        end_date: str,
    ) -> Optional[List[GetMoodOutputDTO]]:
        """
        Get mood history for a user.

        Args:
            user_id: The user's ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).

        Returns:
            List of mood entries, or None if not found.
        """
        query = GetMoodQueryDTO(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )
        results = await self._repository.get_moods(query)
        if results is None:
            return None
        return [GetMoodOutputDTO(**mood) for mood in results]

    async def update_mood(
        self,
        user_id: int,
        date: str,
        emotion: str,
        percentage: float,
    ) -> Optional[GetMoodOutputDTO]:
        """
        Update a mood entry.

        Args:
            user_id: The user's ID.
            date: The date (YYYY-MM-DD).
            emotion: The emotion type.
            percentage: The new percentage.

        Returns:
            GetMoodOutputDTO: Updated mood information, or None if not found.
        """
        command = UpdateMoodCommandDTO(
            user_id=user_id,
            date=date,
            emotion=emotion,
            percentage=percentage,
        )
        result = await self._repository.update_mood(command)
        if result is None:
            return None
        return GetMoodOutputDTO(**result)

    async def delete_mood(self, user_id: int, date: str) -> bool:
        """
        Delete mood entries for a date.

        Args:
            user_id: The user's ID.
            date: The date (YYYY-MM-DD).

        Returns:
            True if deleted successfully.
        """
        command = DeleteMoodCommandDTO(user_id=user_id, date=date)
        return await self._repository.delete_mood(command)
