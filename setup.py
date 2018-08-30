from setuptools import setup

setup(
    name='distributed-asgi',
    description="Create distributed ASGI applications that pull events from a central Redis queue.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ian Murphy",
    author_email="3jackdaws@gmail.com",
    version='0.0.3dev',
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