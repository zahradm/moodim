"""
User controller for handling user-related API endpoints.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from src.configs.containers import get_container, ServiceContainer
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_dtos import (
    CreateUserInputDTO,
    CreateUserOutputDTO,
    GetUserOutputDTO,
    UpdateUserInputDTO,
    UserListItemDTO,
)


logger = logging.getLogger(__name__)
router = APIRouter()


def get_user_logic() -> UserLogic:
    """Dependency to get user logic instance."""
    return get_container().user_logic


@router.post(
    "/",
    response_model=CreateUserOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with email, name, and password.",
)
async def create_user(
    input_dto: CreateUserInputDTO,
    logic: UserLogic = Depends(get_user_logic),
) -> CreateUserOutputDTO:
    """
    Create a new user.

    Args:
        input_dto: User data for creation
        logic: User logic dependency

    Returns:
        CreateUserOutputDTO: Created user information

    Raises:
        HTTPException: If user creation fails
    """
    try:
        return await logic.create_user(input_dto=input_dto)
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User creation failed",
        )


@router.get(
    "/{user_id}",
    response_model=GetUserOutputDTO,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID.",
)
async def get_user(
    user_id: int,
    logic: UserLogic = Depends(get_user_logic),
) -> GetUserOutputDTO:
    """
    Get a user by ID.

    Args:
        user_id: The user's ID
        logic: User logic dependency

    Returns:
        GetUserOutputDTO: User information

    Raises:
        HTTPException: If user not found
    """
    result = await logic.get_user(user_id=user_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result


@router.get(
    "/",
    response_model=List[UserListItemDTO],
    summary="List all users",
    description="Retrieve a list of all users.",
)
async def list_users(
    logic: UserLogic = Depends(get_user_logic),
) -> List[UserListItemDTO]:
    """
    List all users.

    Args:
        logic: User logic dependency

    Returns:
        List of users
    """
    return await logic.get_all_users()


@router.put(
    "/{user_id}",
    response_model=GetUserOutputDTO,
    summary="Update user",
    description="Update an existing user's information.",
)
async def update_user(
    user_id: int,
    input_dto: UpdateUserInputDTO,
    logic: UserLogic = Depends(get_user_logic),
) -> GetUserOutputDTO:
    """
    Update a user.

    Args:
        user_id: The user's ID
        input_dto: Updated user data
        logic: User logic dependency

    Returns:
        GetUserOutputDTO: Updated user information

    Raises:
        HTTPException: If user not found or update fails
    """
    try:
        result = await logic.update_user(user_id=user_id, input_dto=input_dto)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User update failed",
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by their ID.",
)
async def delete_user(
    user_id: int,
    logic: UserLogic = Depends(get_user_logic),
) -> Response:
    """
    Delete a user.

    Args:
        user_id: The user's ID
        logic: User logic dependency

    Returns:
        204 No Content response

    Raises:
        HTTPException: If user not found
    """
    # Check if user exists first
    user = await logic.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await logic.delete_user(user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
