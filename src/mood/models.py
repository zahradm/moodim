from sqlalchemy import Column, Date, Double, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import expression as sql

from src.mood import schemas

Base = declarative_base()


emotion_enum = ENUM(
    "HAPPINESS", "SADNESS", "FEAR", "ANGER", name="emotion_enum", create_type=True
)


class Mood(Base):
    __tablename__ = "mood"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    emotion = Column(emotion_enum, nullable=False)
    percentage = Column(Double, nullable=False)
    date = Column(Date, nullable=False)

    @classmethod
    async def get_moods(cls, db, user_id, start_date, end_date):
        query = sql.select(cls).where(
            cls.user_id == user_id, cls.date >= start_date, cls.date <= end_date
        )
        result = await db.engine.execute(query)
        moods = result.scalar_one_or_none()
        if moods:
            return [schemas.MoodSerializer.from_orm(mood) for mood in moods]
        return None

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
    async def update_mood(cls, db, user_id, date, **kwargs):
        query = (
            sql.update(cls)
            .where(cls.user_id == user_id, cls.date == date)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.emotion, cls.percentage, cls.date)
        )
        result = await db.execute(query)
        await db.commit()
        updated_mood = result.first()
        return schemas.MoodSerializer.from_orm(updated_mood).dict()

    @classmethod
    async def delete_mood(cls, db, user_id, date):
        query = (
            sql.delete(cls)
            .where(cls.user_id == user_id, cls.date == date)
            .returning(cls.id, cls.email)
        )
        await db.execute(query)
        await db.commit()
        return True
