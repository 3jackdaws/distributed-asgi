#!/bin/bash
uvicorn --host "0.0.0.0" --port 80 examples.distributor.distributor:app