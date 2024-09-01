import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db
from src.mood import models, schemas


logger = logging.getLogger(__name__)
api = APIRouter(prefix="/moods")


logger = logging.getLogger(__name__)
api = APIRouter(prefix="/mood")


@api.post("/", response_model=dict)
async def insert_mood(user: schemas.MoodSchema, db: AsyncSession = Depends(db.get_db)):
    try:
        new_mood = await models.Mood.insert_mood(db, **user.dict())
        return new_mood
    except Exception as e:
        logger.error(f"Failed to create mood: {e}")
        raise HTTPException(status_code=400, detail="Insert mood failed")


@api.put("/{user_id}-{data}", response_model=dict)
async def update_mood(
    user_id: int,
    date: str,
    mood: schemas.MoodSchema,
    db: AsyncSession = Depends(db.get_db),
):
    try:
        updated_mood = await models.Mood.update_mood(db, user_id, date, **mood.dict())
        if updated_mood is None:
            raise HTTPException(status_code=404, detail="There is nothing to update")
        return updated_mood
    except Exception as e:
        logger.error(f"Failed to update mood: {e}")
        raise HTTPException(status_code=400, detail="Mood update failed")


@api.get("/{user_id}-{start_date}-{end_date}", response_model=dict)
async def get_mood(
    user_id: int, start_date: str, end_date: str, db: AsyncSession = Depends(db.get_db)
):
    moods = await models.Mood.get_moods(db, user_id, start_date, end_date)
    if moods is None:
        raise HTTPException(status_code=404, detail="Mood not found")
    return moods


@api.delete("/{user_id}-{start_date}-{end_date}", response_model=dict)
async def delete_user(
    user_id: int, start_date: str, end_date: str, db: AsyncSession = Depends(db.get_db)
):
    moods = await models.Mood.get_moods(db, user_id, start_date, end_date)
    if moods is None:
        raise HTTPException(status_code=404, detail="User not found")
    for mood in moods:
        await models.Mood.delete_mood(db, user_id, mood.date)
        return {"detail": "Mood deleted successfully"}
