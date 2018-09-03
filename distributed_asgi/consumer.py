import aioredis
import asyncio
import marshal

from .common import ASGI_EVENTS_KEY_PREFIX


def create_receive(channel_name, redis):
    async def receive():
        return marshal.loads((await redis.blpop(channel_name))[1])
    return receive


def create_send(channel_name, redis):
    async def send(event:dict):
        return redis.rpush(channel_name, marshal.dumps(event))
    return send


class Node:
    def __init__(self, host='localhost', port='6379', key_prefix=ASGI_EVENTS_KEY_PREFIX, cls=None, db=None, password=None):
        self.redis_options = {
            "address" : f"redis://{host}:{port}",
            "db"      : db,
            "password": password
        }
        self.cls        = cls
        self.key_prefix = key_prefix

    async def _run(self):
        self.redis      = await aioredis.create_redis(**self.redis_options)
        app             = self.cls
        while True:
            message     = await self.get_event()
            instance    = app(message['scope'])

            recv_channel, send_channel = message['channels']

            await self.send_worker_info(send_channel)

            receive_coroutine = create_receive(recv_channel, self.redis)
            send_coroutine    = create_send(send_channel, self.redis)

            await instance(receive_coroutine, send_coroutine)
            await self.terminate_asgi(send_channel)

        # Blocking call that runs workers
    def run(self):
        asyncio.get_event_loop().run_until_complete(self._run())

    async def terminate_asgi(self, send_channel):
        await self.redis.rpush(send_channel, marshal.dumps({"type": "app.terminate"}))

    async def send_worker_info(self, send_channel):
        await self.redis.rpush(send_channel, marshal.dumps({"worker": 1}))

    async def get_event(self):
        (
            channel_name,
            raw_message
        ) = await self.redis.blpop(f"{self.key_prefix}-EVENTS")
        return marshal.loads(raw_message)



