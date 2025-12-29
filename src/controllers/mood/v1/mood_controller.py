"""
Mood controller for handling mood-related API endpoints.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from src.configs.containers import get_container
from src.logics.mood.mood_logic import MoodLogic
from src.models.dtos.mood.domain.v1.mood_domain_dtos import (
    CreateMoodInputDTO,
    CreateMoodOutputDTO,
    GetMoodOutputDTO,
    UpdateMoodInputDTO,
)


logger = logging.getLogger(__name__)
router = APIRouter()


def get_mood_logic() -> MoodLogic:
    """Dependency to get mood logic instance."""
    return get_container().mood_logic


@router.post(
    "/",
    response_model=CreateMoodOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new mood entry",
    description="Record a new mood entry for a user.",
)
async def create_mood(
    input_dto: CreateMoodInputDTO,
    logic: MoodLogic = Depends(get_mood_logic),
) -> CreateMoodOutputDTO:
    """
    Create a new mood entry.

    Args:
        input_dto: Mood data for creation
        logic: Mood logic dependency

    Returns:
        CreateMoodOutputDTO: Created mood information

    Raises:
        HTTPException: If mood creation fails
    """
    try:
        return await logic.insert_mood(input_dto=input_dto)
    except Exception as e:
        logger.error(f"Failed to create mood: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mood creation failed",
        )


@router.get(
    "/{user_id}/{start_date}/{end_date}",
    response_model=List[GetMoodOutputDTO],
    summary="Get mood history",
    description="Retrieve mood history for a user within a date range.",
)
async def get_moods(
    user_id: int,
    start_date: str,
    end_date: str,
    logic: MoodLogic = Depends(get_mood_logic),
) -> List[GetMoodOutputDTO]:
    """
    Get mood history for a user.

    Args:
        user_id: The user's ID
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        logic: Mood logic dependency

    Returns:
        List of mood entries

    Raises:
        HTTPException: If no moods found
    """
    result = await logic.get_moods(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood not found",
        )
    return result


@router.put(
    "/{user_id}/{date}/{emotion}",
    response_model=GetMoodOutputDTO,
    summary="Update mood entry",
    description="Update an existing mood entry.",
)
async def update_mood(
    user_id: int,
    date: str,
    emotion: str,
    input_dto: UpdateMoodInputDTO,
    logic: MoodLogic = Depends(get_mood_logic),
) -> GetMoodOutputDTO:
    """
    Update a mood entry.

    Args:
        user_id: The user's ID
        date: The date (YYYY-MM-DD)
        emotion: The emotion type
        input_dto: Updated mood data
        logic: Mood logic dependency

    Returns:
        GetMoodOutputDTO: Updated mood information

    Raises:
        HTTPException: If mood not found or update fails
    """
    try:
        if input_dto.percentage is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Percentage must be provided",
            )

        result = await logic.update_mood(
            user_id=user_id,
            date=date,
            emotion=emotion,
            percentage=input_dto.percentage,
        )
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mood not found or nothing to update",
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update mood: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mood update failed",
        )


@router.delete(
    "/{user_id}/{date}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete mood entries",
    description="Delete all mood entries for a user on a specific date.",
)
async def delete_mood(
    user_id: int,
    date: str,
    logic: MoodLogic = Depends(get_mood_logic),
) -> Response:
    """
    Delete mood entries for a date.

    Args:
        user_id: The user's ID
        date: The date (YYYY-MM-DD)
        logic: Mood logic dependency

    Returns:
        204 No Content response

    Raises:
        HTTPException: If mood not found
    """
    result = await logic.delete_mood(user_id=user_id, date=date)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mood not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
