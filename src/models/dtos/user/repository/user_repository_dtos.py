"""
User repository DTOs.
"""

from typing import Optional

from pydantic import BaseModel


class CreateUserCommandDTO(BaseModel):
    """Command DTO for creating a user in the repository."""

    email: str
    first_name: str
    last_name: str
    password: str


class GetUserQueryDTO(BaseModel):
    """Query DTO for getting a user from the repository."""

    id: int


class UpdateUserCommandDTO(BaseModel):
    """Command DTO for updating a user in the repository."""

    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


class DeleteUserCommandDTO(BaseModel):
    """Command DTO for deleting a user from the repository."""

    id: int
