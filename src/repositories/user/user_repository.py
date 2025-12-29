"""
User repository for orchestrating user data access.
"""

from typing import Any, Dict, List, Optional

from src.models.dtos.user.repository.user_repository_dtos import (
    CreateUserCommandDTO,
    DeleteUserCommandDTO,
    GetUserQueryDTO,
    UpdateUserCommandDTO,
)

from src.repositories.user.adapters.user_postgres_adapter import UserPostgresAdapter


class UserRepository:
    """
    Repository layer for user operations.

    This repository orchestrates data access through adapters,
    providing a clean interface for the business logic layer.
    """

    def __init__(self, postgres_adapter: UserPostgresAdapter) -> None:
        """
        Initialize the repository.

        Args:
            postgres_adapter: PostgreSQL adapter for user operations.
        """
        self._postgres_adapter = postgres_adapter

    async def create_user(self, command: CreateUserCommandDTO) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            command: User creation command.

        Returns:
            Created user data.
        """
        return await self._postgres_adapter.create_user(command)

    async def get_user(self, query: GetUserQueryDTO) -> Optional[Dict[str, Any]]:
        """
        Get a user by ID.

        Args:
            query: User query.

        Returns:
            User data or None.
        """
        return await self._postgres_adapter.get_user(query)

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users.

        Returns:
            List of user data.
        """
        return await self._postgres_adapter.get_all_users()

    async def update_user(
        self, command: UpdateUserCommandDTO
    ) -> Optional[Dict[str, Any]]:
        """
        Update a user.

        Args:
            command: User update command.

        Returns:
            Updated user data or None.
        """
        return await self._postgres_adapter.update_user(command)

    async def delete_user(self, command: DeleteUserCommandDTO) -> bool:
        """
        Delete a user.

        Args:
            command: User delete command.

        Returns:
            True if deleted.
        """
        return await self._postgres_adapter.delete_user(command)
