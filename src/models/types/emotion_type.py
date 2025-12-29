"""
Emotion type enumeration.
"""

from enum import Enum


class EmotionType(str, Enum):
    """Enumeration of supported emotion types."""

    HAPPINESS = "HAPPINESS"
    SADNESS = "SADNESS"
    FEAR = "FEAR"
    ANGER = "ANGER"


class ApiRouterType(str, Enum):
    """Enumeration of API router types for tagging."""

    USER = "👤 Users"
    MOOD = "😊 Moods"
