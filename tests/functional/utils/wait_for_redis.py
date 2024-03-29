import asyncio

import aioredis
import repackage

repackage.up()
from settings import SETTINGS, logger


async def wait_redis():
    client = await aioredis.create_redis_pool((SETTINGS.redis_host, SETTINGS.redis_port), minsize=10, maxsize=20)
    response = await client.ping()
    while not response:
        await asyncio.sleep(2)
        logger.info("Redis is unavailable - sleeping")
        response = await client.ping()
    logger.info("Redis is run")

if __name__ == '__main__':
    repackage.up()
    from settings import SETTINGS, logger
    asyncio.run(wait_redis())

