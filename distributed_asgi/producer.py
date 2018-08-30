import logging
import aioredis
import uuid
import asyncio
import marshal
from .common import ASGI_EVENTS_KEY_PREFIX



def print(*args):
    logging.getLogger().info(*args)


class Distributor:
    key_prefix = ASGI_EVENTS_KEY_PREFIX
    redis_options = {
        "address": "redis://localhost:6379",
        "password": None
    }

    def __init__(self, scope):
        self.scope = scope
        channel_base = str(uuid.uuid4())
        self.recv_channel       = f"{channel_base}-recv"
        self.send_channel       = f"{channel_base}-send"

    async def __call__(self, receive, send):
        consumer_channel = f"{self.key_prefix}-EVENTS"
        message = {
            "channels": [self.recv_channel, self.send_channel],
            "scope": self.scope
        }
        data = marshal.dumps(message)

        self.redis = await aioredis.create_redis(**self.redis_options)
        await self.redis.lpush(consumer_channel, data)

        recv = asyncio.ensure_future(self.transmit_recv(receive))

        while True:
            key, raw_message = await self.redis.blpop(self.send_channel)
            message = marshal.loads(raw_message)
            if message['type'] == "app.terminate":
                recv.cancel()
                return
            await send(message)

    async def transmit_recv(self, receive):
        while True:
            message = await receive()
            await self.redis.rpush(self.recv_channel, marshal.dumps(message))


def create_distributor(host='localhost', port='6379', db=None, password=None, key_prefix=ASGI_EVENTS_KEY_PREFIX):
    class CustomASGIDistributor(Distributor):
        key_prefix = key_prefix
        redis_options = {
            "address": f"redis://{host}:{port}",
            "password": password,
            "db": db
        }

    return CustomASGIDistributor