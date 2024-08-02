# Ensure this imports the global db instance
import logging

import uvicorn
from fastapi import FastAPI
from src.user import router

logger = logging.getLogger(__name__)


def init_app():
    app = FastAPI()

    app.include_router(router.api, prefix="/api")

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
