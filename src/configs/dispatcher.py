"""
Router dispatcher for the Moodim application.
"""

from fastapi import FastAPI

from src.controllers.mood.v1 import mood_controller

from src.controllers.user.v1 import user_controller


def set_dispatch_routes(app: FastAPI) -> None:
    """
    Set up all API routes for the application.

    Args:
        app: The FastAPI application instance.
    """
    # User routes
    app.include_router(
        router=user_controller.router,
        prefix="/api/v1/users",
        tags=["👤 Users"],
    )

    # Mood routes
    app.include_router(
        router=mood_controller.router,
        prefix="/api/v1/moods",
        tags=["😊 Moods"],
    )
