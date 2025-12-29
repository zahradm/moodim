"""
Pytest configuration and fixtures for unit tests.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_db_session():
    """Create a mock database session."""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def mock_user_repository():
    """Create a mock user repository."""
    repo = AsyncMock()
    repo.create_user = AsyncMock()
    repo.get_user = AsyncMock()
    repo.get_all_users = AsyncMock()
    repo.update_user = AsyncMock()
    repo.delete_user = AsyncMock()
    return repo


@pytest.fixture
def mock_mood_repository():
    """Create a mock mood repository."""
    repo = AsyncMock()
    repo.insert_mood = AsyncMock()
    repo.get_mood_by_user_and_date_range = AsyncMock()
    repo.update_mood = AsyncMock()
    repo.delete_mood = AsyncMock()
    return repo


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "SecurePass123!",
    }


@pytest.fixture
def sample_mood_data():
    """Sample mood data for testing."""
    return {
        "user_id": 1,
        "emotion": "HAPPINESS",
        "date": "2025-01-01",
    }
