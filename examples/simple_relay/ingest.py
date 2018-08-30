from distributed_asgi import create_distributor

app = create_distributor(
    key_prefix="MYPREFIX",
    host="mywebsite.com",
    password="abc123"
)
