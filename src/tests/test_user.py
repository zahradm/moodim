"""
Unit tests for User functionality.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.logics.user.user_logic import UserLogic

from src.models.dtos.user.domain.v1.user_domain_dtos import (
    CreateUserInputDTO,
    CreateUserOutputDTO,
    GetUserOutputDTO,
    UpdateUserInputDTO,
)


class TestUserDTOs:
    """Test User DTOs validation."""

    def test_create_user_input_valid(self, sample_user_data):
        """Test valid user creation input."""
        dto = CreateUserInputDTO(**sample_user_data)
        assert dto.email == sample_user_data["email"]
        assert dto.first_name == sample_user_data["first_name"]
        assert dto.last_name == sample_user_data["last_name"]

    def test_create_user_input_invalid_email(self, sample_user_data):
        """Test invalid email validation."""
        sample_user_data["email"] = "invalid-email"
        with pytest.raises(Exception):
            CreateUserInputDTO(**sample_user_data)

    def test_create_user_input_weak_password(self, sample_user_data):
        """Test weak password validation."""
        sample_user_data["password"] = "weak"
        with pytest.raises(Exception):
            CreateUserInputDTO(**sample_user_data)

    def test_create_user_output(self):
        """Test user creation output DTO."""
        dto = CreateUserOutputDTO(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        assert dto.id == 1
        assert dto.email == "test@example.com"


class TestUserLogic:
    """Test User business logic."""

    @pytest.fixture
    def user_logic(self, mock_user_repository):
        """Create UserLogic instance with mock repository."""
        return UserLogic(repository=mock_user_repository)

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, user_logic, mock_user_repository, sample_user_data
    ):
        """Test successful user creation."""
        mock_user_repository.create_user.return_value = {
            "id": 1,
            "email": sample_user_data["email"],
            "first_name": sample_user_data["first_name"],
            "last_name": sample_user_data["last_name"],
        }

        input_dto = CreateUserInputDTO(**sample_user_data)
        result = await user_logic.create_user(input_dto)

        assert result.id == 1
        assert result.email == sample_user_data["email"]
        mock_user_repository.create_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_success(self, user_logic, mock_user_repository):
        """Test successful user retrieval."""
        mock_user_repository.get_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

        result = await user_logic.get_user(1)

        assert result is not None
        assert result.id == 1
        mock_user_repository.get_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, user_logic, mock_user_repository):
        """Test user not found."""
        mock_user_repository.get_user.return_value = None

        result = await user_logic.get_user(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_users(self, user_logic, mock_user_repository):
        """Test get all users."""
        mock_user_repository.get_all_users.return_value = [
            {
                "id": 1,
                "email": "user1@example.com",
                "first_name": "User",
                "last_name": "One",
            },
            {
                "id": 2,
                "email": "user2@example.com",
                "first_name": "User",
                "last_name": "Two",
            },
        ]

        result = await user_logic.get_all_users()

        assert len(result) == 2
        mock_user_repository.get_all_users.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_logic, mock_user_repository):
        """Test successful user deletion."""
        mock_user_repository.delete_user.return_value = True

        result = await user_logic.delete_user(1)

        assert result is True
        mock_user_repository.delete_user.assert_called_once()
