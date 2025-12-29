"""
Unit tests for Mood functionality.
"""

from datetime import date
from unittest.mock import AsyncMock

import pytest

from src.logics.mood.mood_logic import MoodLogic

from src.models.dtos.mood.domain.v1.mood_domain_dtos import (
    CreateMoodInputDTO,
    CreateMoodOutputDTO,
    EmotionType,
    GetMoodOutputDTO,
)


class TestMoodDTOs:
    """Test Mood DTOs validation."""

    def test_create_mood_input_valid(self):
        """Test valid mood creation input."""
        dto = CreateMoodInputDTO(
            user_id=1,
            emotion=EmotionType.HAPPINESS,
            percentage=75.5,
            date=date(2025, 1, 1),
        )
        assert dto.user_id == 1
        assert dto.emotion == EmotionType.HAPPINESS
        assert dto.percentage == 75.5

    def test_create_mood_output(self):
        """Test mood creation output DTO."""
        dto = CreateMoodOutputDTO(
            id=1,
            user_id=1,
            emotion="SADNESS",
            percentage=50.0,
            date=date(2025, 1, 1),
        )
        assert dto.id == 1
        assert dto.emotion == "SADNESS"


class TestEmotionType:
    """Test EmotionType enum."""

    def test_emotion_types_exist(self):
        """Test that all emotion types are defined."""
        assert hasattr(EmotionType, "HAPPINESS")
        assert hasattr(EmotionType, "SADNESS")
        assert hasattr(EmotionType, "FEAR")
        assert hasattr(EmotionType, "ANGER")

    def test_emotion_values(self):
        """Test emotion type values."""
        assert EmotionType.HAPPINESS.value == "HAPPINESS"
        assert EmotionType.SADNESS.value == "SADNESS"
        assert EmotionType.FEAR.value == "FEAR"
        assert EmotionType.ANGER.value == "ANGER"


class TestMoodLogic:
    """Test Mood business logic."""

    @pytest.fixture
    def mood_logic(self, mock_mood_repository):
        """Create MoodLogic instance with mock repository."""
        return MoodLogic(repository=mock_mood_repository)

    @pytest.mark.asyncio
    async def test_insert_mood_success(self, mood_logic, mock_mood_repository):
        """Test successful mood insertion."""
        mock_mood_repository.insert_mood.return_value = {
            "id": 1,
            "user_id": 1,
            "emotion": "HAPPINESS",
            "percentage": 80.0,
            "date": date(2025, 1, 1),
        }

        input_dto = CreateMoodInputDTO(
            user_id=1,
            emotion=EmotionType.HAPPINESS,
            percentage=80.0,
            date=date(2025, 1, 1),
        )
        result = await mood_logic.insert_mood(input_dto)

        assert result.id == 1
        assert result.user_id == 1
        mock_mood_repository.insert_mood.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_moods(self, mood_logic, mock_mood_repository):
        """Test getting moods by date range."""
        mock_mood_repository.get_moods.return_value = [
            {
                "id": 1,
                "user_id": 1,
                "emotion": "HAPPINESS",
                "percentage": 75.0,
                "date": date(2025, 1, 1),
            },
            {
                "id": 2,
                "user_id": 1,
                "emotion": "SADNESS",
                "percentage": 40.0,
                "date": date(2025, 1, 2),
            },
        ]

        result = await mood_logic.get_moods(
            user_id=1,
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        assert len(result) == 2
        mock_mood_repository.get_moods.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_mood_success(self, mood_logic, mock_mood_repository):
        """Test successful mood deletion."""
        mock_mood_repository.delete_mood.return_value = True

        result = await mood_logic.delete_mood(user_id=1, date="2025-01-01")

        assert result is True
        mock_mood_repository.delete_mood.assert_called_once()
