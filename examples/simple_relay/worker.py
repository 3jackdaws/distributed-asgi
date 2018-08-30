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


app = Node(
    host="mywebsite.com",
    port="6379",
    password="abc123",
    cls=ASGIApp,
    key_prefix='MYPREFIX'
)

print(f"Starting worker")
app.run()
