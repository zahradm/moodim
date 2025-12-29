"""
Mood PostgreSQL adapter for database operations.
"""

import datetime
import json
from typing import Any, Dict, List, Optional

import aioredis
from sqlalchemy.sql import expression as sql

from src.configs.runtime_config import RuntimeConfig

from src.core.db import DatabaseSessionManager
from src.models.dtos.mood.repository.mood_repository_dtos import (
    CreateMoodCommandDTO,
    DeleteMoodCommandDTO,
    GetMoodQueryDTO,
    UpdateMoodCommandDTO,
)
from src.models.entities.mood_entity import MoodEntity

CACHE_EXPIRATION_TIME = 60 * 60  # 1 hour


class MoodPostgresAdapter:
    """
    PostgreSQL adapter for mood database operations.

    This adapter handles all direct database interactions for the mood entity,
    including Redis caching for read operations.
    """

    def __init__(self) -> None:
        """Initialize the adapter with database session manager."""
        self._db_manager = DatabaseSessionManager()
        self._db_manager.init_db()
        self._config = RuntimeConfig.global_config()
        self._redis_client = aioredis.from_url(self._config.redis.url)

    async def insert_mood(self, command: CreateMoodCommandDTO) -> Dict[str, Any]:
        """
        Insert a new mood entry.

        Args:
            command: Mood creation command DTO.

        Returns:
            Dictionary with created mood data.
        """
        async with self._db_manager.session() as session:
            query = (
                sql.insert(MoodEntity)
                .values(
                    user_id=command.user_id,
                    emotion=command.emotion,
                    percentage=command.percentage,
                    date=command.date,
                )
                .returning(
                    MoodEntity.id,
                    MoodEntity.user_id,
                    MoodEntity.emotion,
                    MoodEntity.percentage,
                    MoodEntity.date,
                )
            )
            result = await session.execute(query)
            await session.commit()
            row = result.first()
            return {
                "id": row.id,
                "user_id": row.user_id,
                "emotion": row.emotion,
                "percentage": row.percentage,
                "date": row.date,
            }

    async def get_moods(
        self, query_dto: GetMoodQueryDTO
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get moods for a user within a date range.

        Args:
            query_dto: Mood query DTO.

        Returns:
            List of mood data, or None if not found.
        """
        cache_key = f"moods:{query_dto.user_id}"

        # Try to get from cache
        cached_moods = await self._redis_client.get(cache_key)
        if cached_moods:
            return json.loads(cached_moods)

        # Query database
        async with self._db_manager.session() as session:
            start_date = datetime.datetime.strptime(
                query_dto.start_date, "%Y-%m-%d"
            ).date()
            end_date = datetime.datetime.strptime(query_dto.end_date, "%Y-%m-%d").date()

            query = sql.select(MoodEntity).where(
                MoodEntity.user_id == query_dto.user_id,
                MoodEntity.date >= start_date,
                MoodEntity.date <= end_date,
            )
            result = await session.execute(query)
            moods = result.scalars().all()

            if not moods:
                return None

            moods_data = [
                {
                    "user_id": mood.user_id,
                    "emotion": mood.emotion,
                    "percentage": mood.percentage,
                    "date": mood.date.strftime("%Y-%m-%d"),
                }
                for mood in moods
            ]

            # Cache the results
            await self._redis_client.set(
                cache_key,
                json.dumps(moods_data),
                ex=CACHE_EXPIRATION_TIME,
            )

            return moods_data

    async def update_mood(
        self, command: UpdateMoodCommandDTO
    ) -> Optional[Dict[str, Any]]:
        """
        Update a mood entry.

        Args:
            command: Mood update command DTO.

        Returns:
            Dictionary with updated mood data, or None if not found.
        """
        async with self._db_manager.session() as session:
            date_obj = datetime.datetime.strptime(command.date, "%Y-%m-%d").date()

            query = (
                sql.update(MoodEntity)
                .where(
                    MoodEntity.user_id == command.user_id,
                    MoodEntity.date == date_obj,
                    MoodEntity.emotion == command.emotion,
                )
                .values(percentage=command.percentage)
                .returning(
                    MoodEntity.user_id,
                    MoodEntity.emotion,
                    MoodEntity.percentage,
                    MoodEntity.date,
                )
            )
            result = await session.execute(query)
            await session.commit()
            row = result.first()

            if row:
                # Invalidate cache
                cache_key = f"moods:{command.user_id}"
                await self._redis_client.delete(cache_key)

                return {
                    "user_id": row.user_id,
                    "emotion": row.emotion,
                    "percentage": row.percentage,
                    "date": row.date,
                }
            return None

    async def delete_mood(self, command: DeleteMoodCommandDTO) -> bool:
        """
        Delete mood entries for a date.

        Args:
            command: Mood delete command DTO.

        Returns:
            True if deleted successfully.
        """
        async with self._db_manager.session() as session:
            date_obj = datetime.datetime.strptime(command.date, "%Y-%m-%d").date()

            query = (
                sql.delete(MoodEntity)
                .where(
                    MoodEntity.user_id == command.user_id,
                    MoodEntity.date == date_obj,
                )
                .returning(MoodEntity.id)
            )
            result = await session.execute(query)
            await session.commit()

            # Invalidate cache
            cache_key = f"moods:{command.user_id}"
            await self._redis_client.delete(cache_key)

            return result.rowcount > 0
