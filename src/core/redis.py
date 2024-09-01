from typing import Optional

import aioredis
from aioredis import Redis


redis_client: Optional[Redis] = None


async def init_redis_pool():
    global redis_client
    redis_client = await aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )


async def close_redis_pool():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
