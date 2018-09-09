from .producer import Distributor, ASGI_EVENTS_KEY_PREFIX, create_distributor
import aioredis
import re


def _get_key(path, routes:{}):
    for pattern, key_template in routes.items():
        match = pattern.match(path)
        if match:
            return match.expand(key_template)
    return None



def PathDistributor(
        host='localhost',
        port='6379',
        db=None,
        password=None,
        routes={"(*)": "{}"}
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



