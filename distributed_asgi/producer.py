import logging
import aioredis
import uuid
import asyncio
import marshal
import re
from .common import ASGI_EVENTS_KEY_PREFIX, send_error
from concurrent.futures import CancelledError

logger = logging.getLogger()


def print(*args):
    logging.getLogger().info(*args)


class Distributor:
    key = ASGI_EVENTS_KEY_PREFIX
    worker_timeout = 5
    redis_options = {
        "address": "redis://localhost:6379",
        "password": None
    }

    def __init__(self, scope):
        self.scope = scope
        channel_base = str(uuid.uuid4()).replace("-", "")
        self.recv_channel       = f"{channel_base}-recv"
        self.send_channel       = f"{channel_base}-send"
        self.recv_future        = None  # type: asyncio.Future
        self.worker_info        = None

    async def __call__(self, receive, send):
        consumer_channel = str(self.key)
        message = {
            "channels": [self.recv_channel, self.send_channel],
            "scope": self.scope
        }
        data = marshal.dumps(message)

        self.redis = await aioredis.create_redis(**self.redis_options)

        # Push ASGI Event onto Redis queue
        await self.redis.rpush(consumer_channel, data)

        # Start forwarding events
        self.recv_future = asyncio.ensure_future(self.handle_recv(receive))

        # Wait for reply that worker has received event
        response = await self.redis.blpop(self.send_channel, timeout=self.worker_timeout)
        if response is None:
            await send_error(send, 504, b"Worker Timeout")
            logger.warning(f"No workers responded to [{self.key}] event")
            self.stop()
        else:
            self.worker_info = marshal.loads(response[1])
            await self.handle_send(send)


    async def handle_recv(self, receive):
        while True:
            try:
                message = await receive()
                await self.redis.rpush(self.recv_channel, marshal.dumps(message))
            except Exception as e:
                if type(e) is not CancelledError:
                    logger.error(f"[RECV] {str(e)}")

    async def handle_send(self, send):
        while True:
            try:
                key, raw_message = await self.redis.blpop(self.send_channel)
                message = marshal.loads(raw_message)
                if message['type'] == "app.terminate":
                    self.stop()
                    break
                await send(message)
            except Exception as e:
                if type(e) is not CancelledError:
                    logger.error(f"[SEND] {str(e)}")

    def stop(self):
        self.recv_future.cancel() if self.recv_future else None




def create_distributor(host='localhost', port='6379', db=None, password=None, key=ASGI_EVENTS_KEY_PREFIX):
    x = key
    class ASGIDistributor(Distributor):
        key = x
        redis_options = {
            "address": f"redis://{host}:{port}",
            "password": password,
            "db": db
        }

    return ASGIDistributor




def _get_key(path, routes:{}):
    for pattern, key_template in routes.items():
        match = pattern.match(path)
        if match:
            return match.expand(key_template)
    return None



def create_path_distributor(
        host='localhost',
        port='6379',
        db=None,
        password=None,
        routes={".*": "ALL"}
    ):
    routes = {re.compile(pattern):template for pattern, template in routes.items()}
    def return_distributor(scope):
        queue_key = _get_key(scope['path'], routes)

        return create_distributor(
            host,
            port,
            db,
            password,
            key=queue_key
        )(scope)

    return return_distributor