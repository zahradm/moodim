"""
Runtime configuration for the Moodim application.
"""

import os
from dataclasses import dataclass

from dynaconf import Dynaconf

# Get the path to src/core where settings files are located
current_directory = os.path.dirname(os.path.realpath(__file__))
core_directory = os.path.join(os.path.dirname(current_directory), "core")

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        f"{core_directory}/settings.toml",
        f"{core_directory}/.secrets.toml",
    ],
)


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """Database configuration settings."""

    username: str
    password: str
    host: str
    port: str
    db_name: str

    @property
    def async_url(self) -> str:
        """Get async database URL."""
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    @property
    def sync_url(self) -> str:
        """Get sync database URL."""
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(frozen=True, slots=True)
class RedisConfig:
    """Redis configuration settings."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def url(self) -> str:
        """Get Redis URL."""
        return f"redis://{self.host}:{self.port}/{self.db}"


@dataclass(frozen=True, slots=True)
class FastAPIConfig:
    """FastAPI configuration settings."""

    project_name: str = "Moodim"
    version: str = "1.0.0"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    serve_host: str = "127.0.0.1"
    serve_port: int = 8000
    reload: bool = True


class RuntimeConfig:
    """Application runtime configuration."""

    _instance: "RuntimeConfig | None" = None

    def __init__(self) -> None:
        self.database = DatabaseConfig(
            username=settings.db.user_name,
            password=settings.db.password,
            host=settings.db.host,
            port=settings.db.port,
            db_name=settings.db.db_name,
        )
        self.redis = RedisConfig()
        self.fastapi = FastAPIConfig()

    @classmethod
    def global_config(cls) -> "RuntimeConfig":
        """Get the global runtime configuration instance."""
        if cls._instance is None:
            cls._instance = RuntimeConfig()
        return cls._instance

    @classmethod
    def set_global(cls, config: "RuntimeConfig") -> None:
        """Set the global runtime configuration instance."""
        cls._instance = config


# Initialize global config
RuntimeConfig.set_global(RuntimeConfig())
