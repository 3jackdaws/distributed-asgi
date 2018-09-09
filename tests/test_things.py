import pytest
from distributed_asgi import create_path_distributor

def test_path_distributor():
    dist = create_path_distributor(routes={
        "/api/([a-z-]+)": r"\1"
    })

    for path, expected_key in [
        ("/api/banana", "banana"),
        ("/banana", None),
        ()
    ]:
        instance = dist({"path":path})
        assert instance.key == expected_key


