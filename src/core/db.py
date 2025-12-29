"""
Database session management for the Moodim application.
"""

import logging
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from src.core import config


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Config:
    """Database configuration from settings."""

    DB_USER = config.config.username
    DB_PASSWORD = config.config.password
    DB_HOST = config.config.host
    DB_PORT = config.config.port
    DB_DATABASE = config.config.db_name
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    logger.info(f"Database configuration: {DB_CONFIG}")


class DatabaseSessionManager:
    """
    Manages database sessions for async operations.

    This class handles the lifecycle of database connections and sessions,
    providing context managers for safe session handling.
    """

    def __init__(self) -> None:
        """Initialize the session manager."""
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker | None = None
        self._session: async_scoped_session | None = None

    def init_db(self) -> None:
        """
        Initialize the database engine and session factory.

        Creates an asynchronous engine with connection pooling
        and sets up the session maker.
        """
        if self.engine is not None:
            return  # Already initialized

        # Creating an asynchronous engine
        self.engine = create_async_engine(
            Config.DB_CONFIG,
            pool_size=100,
            max_overflow=0,
            pool_pre_ping=True,
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        # Creating a scoped session
        self._session = async_scoped_session(
            self.session_maker,
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provide a transactional scope around a series of operations.

        Yields:
            AsyncSession: Database session for operations.
        """
        if self.session_maker is None:
            self.init_db()

        assert self.session_maker is not None, "Session maker not initialized"
        session = self.session_maker()
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        """Close the database engine and dispose of connections."""
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()
        self.engine = None
        self.session_maker = None
        self._session = None


# Initialize the DatabaseSessionManager
sessionmanager = DatabaseSessionManager()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection for database sessions.

    Yields:
        AsyncSession: Database session for request handling.
    """
    sessionmanager.init_db()
    async with sessionmanager.session() as session:
        yield session
