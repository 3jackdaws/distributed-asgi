# Distributed ASGI
Uses Redis to distribute ASGI messages between worker ASGI apps.  Workers can be on different machines, they just must be able to connect to the central Redis server.


# Usage

```py
# server.py
from distributed_asgi import create_distributor

app = create_distributor(
    host="mywebsite.com",
    port=6379,
    db=0,
    password="abc123",
    key_prefix="MYPREFIX"
)

```


```py
# worker.py
from distributed_asgi import Node


class ASGIApp:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200
        })

        await send({
            "type": "http.response.body",
            "body": b"Hello World!"
        })


node = Node(
    host="mywebsite.com",
    port="6379",
    password="abc123",
    cls=ASGIApp,
    key_prefix='MYPREFIX'
)

print(f"Starting worker")
node.run()
```

Once you have `worker.py` and `server.py`, use some interface server to run `server.py`.

```
$ uvicorn server:App
```

and run `worker.py` as a normal python script:

```
$ python worker.py
```

ASGI requests received by the Distributor will be enqueued and later dequeued by the Node class and passed to the provided asgi app worker.  It should be possible to replace `ASGIApp` in `worker.py` with your favorite ASGI application framework.  Maybe Quart for example?



# Future Plans
* Path-based HTTP router that puts requests into different queues based on path.
