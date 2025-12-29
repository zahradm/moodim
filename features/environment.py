"""
Environment configuration for Behave BDD tests.
"""

import asyncio

from behave import fixture, use_fixture
from fastapi.testclient import TestClient

from main import app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Test database configuration
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_moodim"


def get_test_db():
    """Create a test database engine and session."""
    engine = create_engine(
        TEST_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, TestingSessionLocal


def create_tables(engine):
    """Create tables manually to avoid foreign key issues."""
    with engine.connect() as conn:
        # Create user table first
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """
            )
        )

        # Create emotion_enum type
        conn.execute(
            text(
                """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'emotion_enum') THEN
                    CREATE TYPE emotion_enum AS ENUM ('HAPPINESS', 'SADNESS', 'FEAR', 'ANGER');
                END IF;
            END$$;
        """
            )
        )

        # Create mood table with foreign key
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS mood (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id),
                emotion emotion_enum NOT NULL,
                percentage DOUBLE PRECISION NOT NULL,
                date DATE NOT NULL,
                UNIQUE(user_id, date, emotion)
            )
        """
            )
        )
        conn.commit()


def drop_tables(engine):
    """Drop tables in correct order."""
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS mood CASCADE"))
        conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
        conn.execute(text("DROP TYPE IF EXISTS emotion_enum CASCADE"))
        conn.commit()


@fixture
def api_client(context):
    """Fixture to provide FastAPI test client."""
    context.client = TestClient(app)
    yield context.client


@fixture
def database(context):
    """Fixture to provide test database."""
    engine, SessionLocal = get_test_db()

    # Drop and recreate tables for clean state
    drop_tables(engine)
    create_tables(engine)

    context.db_engine = engine
    context.db_session = SessionLocal()

    yield context.db_session

    # Cleanup
    context.db_session.close()
    drop_tables(engine)


def before_all(context):
    """Setup before all tests."""
    context.base_url = "http://localhost:8000"
    context.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(context.loop)


def after_all(context):
    """Cleanup after all tests."""
    context.loop.close()


def before_feature(context, feature):
    """Setup before each feature."""
    use_fixture(api_client, context)
    use_fixture(database, context)


def after_feature(context, feature):
    """Cleanup after each feature."""
    pass


def before_scenario(context, scenario):
    """Setup before each scenario."""
    # Clear any cached data
    context.response = None
    context.request_data = None
    context.created_user_id = None
    context.created_mood_id = None


def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    # Clean up test data if needed
    if hasattr(context, "db_session"):
        context.db_session.rollback()


def before_tag(context, tag):
    """Handle specific tags."""
    if tag == "skip":
        context.scenario.skip("Marked with @skip")
    elif tag == "wip":
        context.scenario.skip("Work in progress")


def after_tag(context, tag):
    """Cleanup after specific tags."""
    pass
