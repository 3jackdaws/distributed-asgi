from setuptools import setup

long_description = ""

try:
    with open("README.md") as fp:
        long_description = fp.read()
except:
    pass

setup(
    name='distributed-asgi',
    description="Create distributed ASGI applications that pull events from a central Redis queue.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/3jackdaws/distributed-asgi",
    author="Ian Murphy",
    author_email="3jackdaws@gmail.com",
    version='0.0.7',
    packages=['distributed_asgi',],
    license='MIT',
    install_requires=[
        "aioredis",
    ],
    tests_require=[
        "pytest"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)