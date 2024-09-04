import datetime
import json

from aioredis import Redis
from sqlalchemy import Column, Date, Double, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import expression as sql

from src.mood import schemas

Base = declarative_base()


emotion_enum = ENUM(
    "HAPPINESS", "SADNESS", "FEAR", "ANGER", name="emotion_enum", create_type=True
)


CACHE_EXPIRATION_TIME = 60 * 60


class Mood(Base):
    __tablename__ = "mood"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    emotion = Column(emotion_enum, nullable=False)
    percentage = Column(Double, nullable=False)
    date = Column(Date, nullable=False)

    @classmethod
    async def insert_mood(cls, db, **kwargs):
        query = (
            sql.insert(cls)
            .values(**kwargs)
            .returning(cls.user_id, cls.emotion, cls.percentage, cls.date)
        )
        result = await db.execute(query)
        await db.commit()
        new = result.first()
        return schemas.MoodSerializer.from_orm(new).dict()

    @classmethod
    async def get_mood(
        cls,
        db,
        user_id: int,
        start_date: str,
        end_date: str,
        redis_client: Redis,
    ):
        cache_key = f"moods:{user_id}"

        cached_moods = await redis_client.get(cache_key)
        if cached_moods:
            return json.loads(cached_moods)

        query = await db.execute(
            sql.select(cls).where(
                cls.user_id == user_id,
                cls.date >= datetime.datetime.strptime(start_date, "%Y-%m-%d"),
                cls.date <= datetime.datetime.strptime(end_date, "%Y-%m-%d"),
            )
        )
        moods = query.scalars().all()

        if moods:
            moods_serializable = [
                {
                    **schemas.MoodSerializer.from_orm(mood).dict(),
                    "date": mood.date.strftime("%Y-%m-%d"),
                }
                for mood in moods
            ]

            await redis_client.set(
                cache_key, json.dumps(moods_serializable), ex=CACHE_EXPIRATION_TIME
            )
            return moods_serializable

        return None

    @classmethod
    async def update_mood(
        cls,
        db,
        user_id: int,
        date: str,
        emotion: str,
        percentage: float,
    ):
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        if not emotion or percentage is None:
            raise ValueError("Both 'emotion' and 'percentage' values must be provided")

        query = (
            sql.update(cls)
            .where(cls.user_id == user_id, cls.date == date_obj, cls.emotion == emotion)
            .values(percentage=percentage)
            .execution_options(synchronize_session="fetch")
            .returning(cls.user_id, cls.emotion, cls.percentage, cls.date)
        )

        result = await db.execute(query)
        await db.commit()
        updated_mood = result.first()

        if updated_mood:
            return schemas.MoodSerializer(
                user_id=updated_mood.user_id,
                emotion=updated_mood.emotion,
                percentage=updated_mood.percentage,
                date=updated_mood.date,
            ).dict()

        return None

    @classmethod
    async def delete_mood(cls, db, user_id, date):
        query = (
            sql.delete(cls)
            .where(cls.user_id == user_id, cls.date == date)
            .returning(cls.id, cls.date)
        )
        await db.execute(query)
        await db.commit()
        return True
