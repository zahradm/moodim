"""
User domain DTOs for API layer.
"""

import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password(value: str) -> str:
    """Validate password strength."""
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[\W]", value):
        raise ValueError("Password must contain at least one special character.")
    return value


class CreateUserInputDTO(BaseModel):
    """DTO for creating a new user."""

    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(..., min_length=2, description="User's first name")
    last_name: str = Field(..., min_length=2, description="User's last name")
    password: str = Field(
        ..., min_length=8, max_length=64, description="User's password"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        return validate_password(value)


class CreateUserOutputDTO(BaseModel):
    """DTO for user creation response."""

    id: int = Field(..., description="User's ID")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")

    class Config:
        from_attributes = True


class GetUserOutputDTO(BaseModel):
    """DTO for getting user details."""

    id: Optional[int] = Field(None, description="User's ID")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")

    class Config:
        from_attributes = True


class UserListItemDTO(BaseModel):
    """DTO for user list item."""

    id: Optional[int] = Field(None, description="User's ID")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")

    class Config:
        from_attributes = True


class UpdateUserInputDTO(BaseModel):
    """DTO for updating a user."""

    first_name: str = Field(..., min_length=2, description="User's first name")
    last_name: str = Field(..., min_length=2, description="User's last name")
    password: str = Field(
        ..., min_length=8, max_length=64, description="User's password"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        return validate_password(value)


class DeleteUserOutputDTO(BaseModel):
    """DTO for user deletion response."""

    detail: str = Field(..., description="Deletion status message")
