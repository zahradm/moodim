"""
Mood domain DTOs for API layer.
"""

import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EmotionType(str, Enum):
    """Emotion type enumeration."""

    HAPPINESS = "HAPPINESS"
    SADNESS = "SADNESS"
    FEAR = "FEAR"
    ANGER = "ANGER"


class CreateMoodInputDTO(BaseModel):
    """DTO for creating a new mood entry."""

    user_id: int = Field(..., description="User's ID")
    emotion: EmotionType = Field(..., description="Emotion type")
    percentage: float = Field(
        ..., ge=0, le=100, description="Emotion intensity percentage"
    )
    date: datetime.date = Field(..., description="Date of the mood entry")


class CreateMoodOutputDTO(BaseModel):
    """DTO for mood creation response."""

    id: int = Field(..., description="Mood entry ID")
    user_id: int = Field(..., description="User's ID")
    emotion: str = Field(..., description="Emotion type")
    percentage: float = Field(..., description="Emotion intensity percentage")
    date: datetime.date = Field(..., description="Date of the mood entry")

    class Config:
        from_attributes = True


class GetMoodOutputDTO(BaseModel):
    """DTO for getting mood details."""

    user_id: int = Field(..., description="User's ID")
    emotion: str = Field(..., description="Emotion type")
    percentage: float = Field(..., description="Emotion intensity percentage")
    date: datetime.date = Field(..., description="Date of the mood entry")

    class Config:
        from_attributes = True


class UpdateMoodInputDTO(BaseModel):
    """DTO for updating a mood entry."""

    user_id: Optional[int] = Field(None, description="User's ID")
    emotion: Optional[str] = Field(None, description="Emotion type")
    percentage: Optional[float] = Field(
        None, ge=0, le=100, description="Emotion intensity percentage"
    )
    date: Optional[datetime.date] = Field(None, description="Date of the mood entry")


class DeleteMoodOutputDTO(BaseModel):
    """DTO for mood deletion response."""

    detail: str = Field(..., description="Deletion status message")
