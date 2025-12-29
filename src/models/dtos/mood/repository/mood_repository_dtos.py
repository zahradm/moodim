"""
Mood repository DTOs.
"""

import datetime

from pydantic import BaseModel


class CreateMoodCommandDTO(BaseModel):
    """Command DTO for creating a mood in the repository."""

    user_id: int
    emotion: str
    percentage: float
    date: datetime.date


class GetMoodQueryDTO(BaseModel):
    """Query DTO for getting moods from the repository."""

    user_id: int
    start_date: str
    end_date: str


class UpdateMoodCommandDTO(BaseModel):
    """Command DTO for updating a mood in the repository."""

    user_id: int
    date: str
    emotion: str
    percentage: float


class DeleteMoodCommandDTO(BaseModel):
    """Command DTO for deleting a mood from the repository."""

    user_id: int
    date: str
