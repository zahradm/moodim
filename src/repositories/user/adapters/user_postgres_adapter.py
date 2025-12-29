"""
User PostgreSQL adapter for database operations.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.sql import expression as sql

from src.core.db import DatabaseSessionManager
from src.models.dtos.user.repository.user_repository_dtos import (
    CreateUserCommandDTO,
    DeleteUserCommandDTO,
    GetUserQueryDTO,
    UpdateUserCommandDTO,
)
from src.models.entities.user_entity import UserEntity


class UserPostgresAdapter:
    """
    PostgreSQL adapter for user database operations.

    This adapter handles all direct database interactions for the user entity.
    """

    def __init__(self) -> None:
        """Initialize the adapter with database session manager."""
        self._db_manager = DatabaseSessionManager()
        self._db_manager.init_db()

    async def create_user(self, command: CreateUserCommandDTO) -> Dict[str, Any]:
        """
        Create a new user in the database.

        Args:
            command: User creation command DTO.

        Returns:
            Dictionary with created user data.
        """
        async with self._db_manager.session() as session:
            query = (
                sql.insert(UserEntity)
                .values(
                    email=command.email,
                    first_name=command.first_name,
                    last_name=command.last_name,
                    password=command.password,
                )
                .returning(
                    UserEntity.id,
                    UserEntity.email,
                    UserEntity.first_name,
                    UserEntity.last_name,
                )
            )
            result = await session.execute(query)
            await session.commit()
            row = result.first()
            return {
                "id": row.id,
                "email": row.email,
                "first_name": row.first_name,
                "last_name": row.last_name,
            }

    async def get_user(self, query_dto: GetUserQueryDTO) -> Optional[Dict[str, Any]]:
        """
        Get a user by ID.

        Args:
            query_dto: User query DTO.

        Returns:
            Dictionary with user data, or None if not found.
        """
        async with self._db_manager.session() as session:
            query = sql.select(UserEntity).where(UserEntity.id == query_dto.id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            return None

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users.

        Returns:
            List of dictionaries with user data.
        """
        async with self._db_manager.session() as session:
            query = sql.select(UserEntity)
            result = await session.execute(query)
            users = result.scalars().all()
            return [
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                for user in users
            ]

    async def update_user(
        self, command: UpdateUserCommandDTO
    ) -> Optional[Dict[str, Any]]:
        """
        Update a user.

        Args:
            command: User update command DTO.

        Returns:
            Dictionary with updated user data, or None if not found.
        """
        async with self._db_manager.session() as session:
            update_data = {}
            if command.first_name:
                update_data["first_name"] = command.first_name
            if command.last_name:
                update_data["last_name"] = command.last_name
            if command.password:
                update_data["password"] = command.password

            if not update_data:
                return None

            query = (
                sql.update(UserEntity)
                .where(UserEntity.id == command.id)
                .values(**update_data)
                .returning(
                    UserEntity.id,
                    UserEntity.email,
                    UserEntity.first_name,
                    UserEntity.last_name,
                )
            )
            result = await session.execute(query)
            await session.commit()
            row = result.first()
            if row:
                return {
                    "id": row.id,
                    "email": row.email,
                    "first_name": row.first_name,
                    "last_name": row.last_name,
                }
            return None

    async def delete_user(self, command: DeleteUserCommandDTO) -> bool:
        """
        Delete a user.

        Args:
            command: User delete command DTO.

        Returns:
            True if deleted successfully.
        """
        async with self._db_manager.session() as session:
            query = (
                sql.delete(UserEntity)
                .where(UserEntity.id == command.id)
                .returning(UserEntity.id)
            )
            await session.execute(query)
            await session.commit()
            return True
