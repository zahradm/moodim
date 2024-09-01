import logging

import uvicorn
from fastapi import FastAPI
from src import mood, user
from src.core.redis import close_redis_pool, init_redis_pool

logger = logging.getLogger(__name__)


def init_app():
    app = FastAPI(lifespan=lifespan)

    app.include_router(user.router.api, prefix="/v1")
    app.include_router(mood.router.api, prefix="/v1")

    return app


async def lifespan(app: FastAPI):
    # Startup
    await init_redis_pool()

    yield  # Control goes to the application

    # Shutdown
    await close_redis_pool()


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
