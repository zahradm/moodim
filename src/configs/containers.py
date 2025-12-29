"""
Dependency injection container for the Moodim application.
"""

from src.configs.runtime_config import RuntimeConfig
from src.logics.mood.mood_logic import MoodLogic
from src.logics.user.user_logic import UserLogic
from src.repositories.mood.adapters.mood_postgres_adapter import MoodPostgresAdapter
from src.repositories.mood.mood_repository import MoodRepository
from src.repositories.user.adapters.user_postgres_adapter import UserPostgresAdapter
from src.repositories.user.user_repository import UserRepository


class ServiceContainer:
    """
    Dependency injection container for managing service instances.

    This container provides singleton instances of logics and repositories
    following the clean architecture pattern.
    """

    _instance: "ServiceContainer | None" = None
    _user_logic: UserLogic | None = None
    _mood_logic: MoodLogic | None = None

    def __init__(self) -> None:
        self._config = RuntimeConfig.global_config()

    @classmethod
    def instance(cls) -> "ServiceContainer":
        """Get the singleton instance of the container."""
        if cls._instance is None:
            cls._instance = ServiceContainer()
        return cls._instance

    @property
    def user_logic(self) -> UserLogic:
        """Get the user logic instance."""
        if self._user_logic is None:
            user_adapter = UserPostgresAdapter()
            user_repository = UserRepository(postgres_adapter=user_adapter)
            self._user_logic = UserLogic(repository=user_repository)
        return self._user_logic

    @property
    def mood_logic(self) -> MoodLogic:
        """Get the mood logic instance."""
        if self._mood_logic is None:
            mood_adapter = MoodPostgresAdapter()
            mood_repository = MoodRepository(postgres_adapter=mood_adapter)
            self._mood_logic = MoodLogic(repository=mood_repository)
        return self._mood_logic


def get_container() -> ServiceContainer:
    """Get the service container instance."""
    return ServiceContainer.instance()
