"""
User business logic layer.
"""

from typing import List, Optional

from src.models.dtos.user.domain.v1.user_domain_dtos import (
    CreateUserInputDTO,
    CreateUserOutputDTO,
    GetUserOutputDTO,
    UpdateUserInputDTO,
    UserListItemDTO,
)
from src.models.dtos.user.repository.user_repository_dtos import (
    CreateUserCommandDTO,
    DeleteUserCommandDTO,
    GetUserQueryDTO,
    UpdateUserCommandDTO,
)
from src.repositories.user.user_repository import UserRepository


class UserLogic:
    """
    Business logic layer for user operations.

    This class contains the business rules and orchestrates
    the flow between controllers and repositories.
    """

    def __init__(self, repository: UserRepository) -> None:
        """
        Initialize the user logic.

        Args:
            repository: The user repository instance.
        """
        self._repository = repository

    async def create_user(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        """
        Create a new user.

        Args:
            input_dto: User data for creation.

        Returns:
            CreateUserOutputDTO: Created user information.
        """
        command = CreateUserCommandDTO(
            email=input_dto.email,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
            password=input_dto.password,
        )
        result = await self._repository.create_user(command)
        return CreateUserOutputDTO(**result)

    async def get_user(self, user_id: int) -> Optional[GetUserOutputDTO]:
        """
        Get a user by ID.

        Args:
            user_id: The user's ID.

        Returns:
            GetUserOutputDTO: User information, or None if not found.
        """
        query = GetUserQueryDTO(id=user_id)
        result = await self._repository.get_user(query)
        if result is None:
            return None
        return GetUserOutputDTO(**result)

    async def get_all_users(self) -> List[UserListItemDTO]:
        """
        Get all users.

        Returns:
            List of users.
        """
        results = await self._repository.get_all_users()
        return [UserListItemDTO(**user) for user in results]

    async def update_user(
        self,
        user_id: int,
        input_dto: UpdateUserInputDTO,
    ) -> Optional[GetUserOutputDTO]:
        """
        Update a user.

        Args:
            user_id: The user's ID.
            input_dto: Updated user data.

        Returns:
            GetUserOutputDTO: Updated user information, or None if not found.
        """
        command = UpdateUserCommandDTO(
            id=user_id,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
            password=input_dto.password,
        )
        result = await self._repository.update_user(command)
        if result is None:
            return None
        return GetUserOutputDTO(**result)

    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: The user's ID.

        Returns:
            True if deleted successfully.
        """
        command = DeleteUserCommandDTO(id=user_id)
        return await self._repository.delete_user(command)
