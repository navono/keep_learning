import asyncio
from dask.distributed import Client


async def create_dask_client():
    return await Client(asynchronous=True)


client = asyncio.run(create_dask_client())
