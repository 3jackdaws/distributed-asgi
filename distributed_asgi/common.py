import aioredis


ASGI_EVENTS_KEY_PREFIX = "ASGI"



async def send_error(send, status, body=b''):
    await send({
        "type": "http.response.start",
        "status": status
    })
    await send({
        "type": "http.response.body",
        "body": body
    })