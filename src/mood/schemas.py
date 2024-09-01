import datetime
from enum import Enum

from pydantic import BaseModel


class EmotionEnum(str, Enum):
    HAPPINESS = "HAPPINESS"
    SADNESS = "SADNESS"
    FEAR = "FEAR"
    ANGER = "ANGER"


class MoodSchema(BaseModel):
    user_id: int
    emotion: EmotionEnum  #
    percentage: float
    date: datetime.date


class MoodSerializer(MoodSchema):
    class Config:
        from_attributes = True
