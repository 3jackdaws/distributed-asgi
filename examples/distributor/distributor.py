from distributed_asgi import Distributor, create_distributor
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASS = os.environ.get("REDIS_PASS")

REDIS_DB   = os.environ.get("REDIS_DB")


KEY_PREFIX = os.environ.get("KEY_PREFIX")



app = create_distributor(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASS,
    key_prefix=KEY_PREFIX
)