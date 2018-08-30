# Distributed ASGI
Uses Redis to distribute ASGI messages between worker ASGI apps.  Workers can be on different machines, they just must be able to connect to the central Redis server.


# Usage
Set custom redis options and key prefixes by subclassing `ASGIRedisProducer`.


```py
# server.py
from distributed_asgi import ASGIRedisProducer

class App(ASGIRedisProducer):
    key_prefix = "MYPREFIX"
    redis_options = {
        "address": "redis://mywebsite.com",
        "password": "abc123"
    }

```


```py
# worker.py
from distributed_asgi import ASGIRedisConsumer


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


app = ASGIRedisConsumer(
    host="mywebsite.com",
    port="6379",
    password="abc123",
    cls=ASGIApp,
    key_prefix='MYPREFIX'
)

print(f"Starting worker")
app.run()
```

Once you have `worker.py` and `server.py`, use some interface server to run `server.py`.

```
$ uvicorn server:App
```

and run `worker.py` as a normal python script:

```
$ python worker.py
```

ASGI requests received by the ASGIRedisProducer will be enqueued and later dequeued by the ASGIRedisConsumer worker.  It should be possible to replace `ASGIApp` in `worker.py` with your favorite ASGI application framework.  Maybe Quart for example?



# Future Plans
* Path-based HTTP router that puts requests into different queues based on path.  Would allow for
