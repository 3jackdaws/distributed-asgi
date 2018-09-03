import sys

sys.path.append("/app")

from distributed_asgi import Node


class ASGIApp:

    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, recieve, send):
        await send({
            "type":"http.response.start",
            "status": 200
        })

        await send({
            "type": "http.response.body",
            "body": b"Hello World!"
        })


print("RUNNING WORKER")
Node(
    host="redis",
    key_prefix='ISO',
    cls=ASGIApp
).run()