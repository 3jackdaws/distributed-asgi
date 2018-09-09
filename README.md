# Distributed ASGI
Uses Redis to distribute ASGI messages between worker ASGI apps based on routes.  Workers can be on different machines, they just must be able to connect to the central Redis server.


# Usage

Routes are made of two parts: a regular expression that matches a path, and a key template string that is used to form the key that ASGI events are pushed to.

Key templates can also use numbered regex backslash replacements.  For example, the route `{"/api/([a-z-]+)":r"API-\1"}` will match and produce the following keys:

```
PATH                KEY
/api/test           API-test
/api/test/38        API-test
/api/banana         API-banana
/test/api/test2     API-test2
```

Here's an example:

```py
# distributor.py
from distributed_asgi import create_path_distributor

app = create_path_distributor(
    host="mywebsite.com",       # point to redis server
    port=6379,
    db=0,
    password="abc123",
    routes={
        "/api/([a-z-]+)": r"ASGI-\1",
        "/worker/([0-9]+)": r"worker-queue-\1",
        "/": "ALL-WEBSITE-TRAFFIC"
    }
)

```

To actually make use of this, we need to make a worker that listens on one or more of the keys


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
    key='ASGI-testing'
)

print(f"Starting worker")
node.run()
```

Once you have `worker.py` and `server.py`, use some interface server to run `distributor.py`.

```
$ uvicorn server:App
```

and run `worker.py` as a normal python script:

```
$ python worker.py
```

The worker will only respond to http requests with a path that contains `/api/testing` because that is the only key we told it to listen to.

# What happens if there are no workers?
If there is no Node instance listening on a key that the Distributor pushes events to, the Distributor will timeout after 5 seconds, close the connection, and return a 405 error.  Workers do not need to respond within 5 seconds, the Node class will automatically let the Distributor know there is a worker at least listening.
