from fastapi import APIRouter

# from .dask_client import client as dask_client
from py_project.utils.dask_client import dask_client

router = APIRouter()


@router.get("/")
async def home():
    # from py_project.app import dask_client
    dask_client.submit(lambda: print("Hello, Dask!"))
    return {'message': 'Hello, FastAPI!'}
