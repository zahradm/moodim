"""
Mood entity for database operations.
"""

from sqlalchemy import Column, Date, Double, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base

Base = declarative_base()

emotion_enum = ENUM(
    "HAPPINESS",
    "SADNESS",
    "FEAR",
    "ANGER",
    name="emotion_enum",
    create_type=True,
)


class MoodEntity(Base):
    """
    Mood entity representing the mood table in the database.

    Attributes:
        id: Primary key.
        user_id: Foreign key to user table.
        emotion: Type of emotion.
        percentage: Intensity percentage (0-100).
        date: Date of the mood entry.
    """

    __tablename__ = "mood"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    emotion = Column(emotion_enum, nullable=False)
    percentage = Column(Double, nullable=False)
    date = Column(Date, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<MoodEntity(id={self.id}, user_id={self.user_id}, emotion={self.emotion})>"

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "emotion": self.emotion,
            "percentage": self.percentage,
            "date": self.date,
        }
