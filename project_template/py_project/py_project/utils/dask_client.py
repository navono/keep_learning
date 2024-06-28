from dask.distributed import Client

dask_client = None


async def start_dask_client():
    global dask_client
    dask_client = await Client(asynchronous=True)
    # dask_client = await Client()


async def stop_dask_client():
    await dask_client.close()
