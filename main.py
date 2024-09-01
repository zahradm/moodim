import logging

import uvicorn
from fastapi import FastAPI
from src import mood, user

logger = logging.getLogger(__name__)


def init_app():
    app = FastAPI()

    app.include_router(user.router.api, prefix="/v1")
    app.include_router(mood.router.api, prefix="/v1")

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
