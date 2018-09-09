from distributed_asgi import Distributor, create_distributor
import os
import aioredis
import asyncio

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASS = os.environ.get("REDIS_PASS")

REDIS_DB   = os.environ.get("REDIS_DB", 0)


KEY_PREFIX = os.environ.get("KEY_PREFIX")

async def check_connectivity():
    redis = await aioredis.create_redis(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        db=REDIS_DB,
        password=REDIS_PASS
    )
    info = await redis.info("server")
    print("REDIS VERSION {} ON {}:{}".format(
        info['server']['redis_version'],
        REDIS_HOST,
        REDIS_PORT
    ))

asyncio.get_event_loop().run_until_complete(check_connectivity())

app = create_distributor(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASS,
    key_prefix=KEY_PREFIX
)