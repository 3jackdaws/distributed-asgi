from uuid import uuid4
from time import time
import os

def get_random_id():
    length = 36
    lower = 33
    upper = 126
    diff = upper - lower
    id = bytearray(os.urandom(length))
    for i, c in enumerate(id):
        id[i] = (c % diff) + lower
    return id

def get_random_id2():
    return str(uuid4()).replace("-", "")


ITERATIONS = 100000

TEST_FUNCTIONS = [
    get_random_id,
    get_random_id2
]

print(len(str(uuid4())))

for generation_function in TEST_FUNCTIONS:
    total = 0
    for _ in range(ITERATIONS):
        start = time()
        id = generation_function()
        duration = time() - start
        total += duration
    avg = total/ITERATIONS

    print(f"AVG: {avg} s")