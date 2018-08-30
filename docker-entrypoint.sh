#!/usr/bin/env bash
uvicorn --host "0.0.0.0" --port "80" asgi_redis:ASGIRedisProducer  &
WORKERS=5

for i in {1..4}; do
    python worker.py $i &
    sleep 1
done
python worker.py 5       