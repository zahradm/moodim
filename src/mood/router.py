import json
import logging
from typing import List

import aioredis

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db
from src.mood import models, schemas

logger = logging.getLogger(__name__)
api = APIRouter(prefix="/mood")

CACHE_EXPIRATION_TIME = 60 * 60
redis_client = aioredis.from_url("redis://localhost")


@api.post("/", response_model=dict)
async def insert_mood(
    user: schemas.MoodSchema,
    db: AsyncSession = Depends(db.get_db),
):
    try:
        new_mood = await models.Mood.insert_mood(db, **user.dict())
        return new_mood
    except Exception as e:
        logger.error(f"Failed to create mood: {e}")
        raise HTTPException(status_code=400, detail="Insert mood failed")


@api.put("/{user_id}/{date}/{emotion}", response_model=dict)
async def update_mood(
    user_id: int,
    date: str,
    emotion: str,
    mood: schemas.MoodSchema,
    db: AsyncSession = Depends(db.get_db),
):
    try:
        if mood.percentage is None:
            raise HTTPException(status_code=400, detail="Percentage must be provided")

        updated_mood = await models.Mood.update_mood(
            db, user_id, date, emotion=emotion, percentage=mood.percentage
        )

        if updated_mood is None:
            raise HTTPException(
                status_code=404, detail="Mood not found or nothing to update"
            )

        return updated_mood
    except Exception as e:
        logger.error(f"Failed to update mood: {e}")
        raise HTTPException(status_code=400, detail="Mood update failed")


@api.get(
    "/{user_id}/{start_date}/{end_date}", response_model=List[schemas.MoodSerializer]
)
async def get_mood(
    user_id: int,
    start_date: str,
    end_date: str,
    db: AsyncSession = Depends(db.get_db),
):
    global redis_client
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    cache_key = f"moods:{user_id}"
    cached_moods = await redis_client.get(cache_key)

    if cached_moods:
        logger.info("Returning cached mood data")
        return json.loads(cached_moods)

    moods = await models.Mood.get_mood(db, user_id, start_date, end_date, redis_client)
    if moods is None:
        raise HTTPException(status_code=404, detail="Mood not found")

    await redis_client.set(cache_key, json.dumps(moods), ex=CACHE_EXPIRATION_TIME)

    return moods


@api.delete("/{user_id}/{date}", response_model=dict)
async def delete_user(
    user_id: int,
    date: str,
    db: AsyncSession = Depends(db.get_db),
):
    moods = await models.Mood.delete_mood(db, user_id, date)
    if moods is None:
        raise HTTPException(status_code=404, detail="User not found")
    for mood in moods:
        await models.Mood.delete_mood(db, user_id, mood.date)
        return {"detail": "Mood deleted successfully"}
