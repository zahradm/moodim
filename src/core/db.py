import logging
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
)

from src.core import config


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Config:
    DB_USER = config.config.username
    DB_PASSWORD = config.config.password
    DB_HOST = config.config.host
    DB_PORT = config.config.port
    DB_DATABASE = config.config.db_name
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    logger.info(f"Database configuration: {DB_CONFIG}")


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.session = None

    def init_db(self):
        # Creating an asynchronous engine
        self.engine = create_async_engine(
            Config.DB_CONFIG, pool_size=100, max_overflow=0, pool_pre_ping=True
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Creating a scoped session
        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    async def close(self):
        # Closing the database session
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()


# Initialize the DatabaseSessionManager
sessionmanager = DatabaseSessionManager()


async def get_db():
    sessionmanager.init_db()  # Initialize the database session manager
    async_session = sessionmanager.session()
    try:
        yield async_session
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await async_session.rollback()
        raise
    finally:
        await async_session.close()
        await sessionmanager.close()
