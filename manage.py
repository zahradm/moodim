"""
Moodim Application Entry Point

This module serves as the main entry point for the Moodim application.
It sets up the FastAPI application with all routes and configurations.
"""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from src.configs.dispatcher import set_dispatch_routes

from src.configs.runtime_config import RuntimeConfig


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="{'time':'%(asctime)s', 'name': '%(name)s', "
    "'level': '%(levelname)s', 'message': '%(message)s'}",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Moodim application...")
    yield
    # Shutdown
    logger.info("Shutting down Moodim application...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    config = RuntimeConfig.global_config()

    app = FastAPI(
        title=config.fastapi.project_name,
        version=config.fastapi.version,
        docs_url=config.fastapi.docs_url,
        redoc_url=config.fastapi.redoc_url,
        lifespan=lifespan,
    )

    # Set up routes
    set_dispatch_routes(app)

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    config = RuntimeConfig.global_config()
    uvicorn.run(
        app="manage:app",
        host=config.fastapi.serve_host,
        port=config.fastapi.serve_port,
        reload=config.fastapi.reload,
    )
