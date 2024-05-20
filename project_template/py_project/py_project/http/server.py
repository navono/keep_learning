from fastapi import FastAPI
import uvicorn
from loguru import logger

app = FastAPI()
app.include_router(handler_router)


class HTTPServer:
    def __init__(self, config=None):
        self.__config = config
        self.host = config['host']
        self.port = config['port']

    async def start(self):
        logger.trace(f"http server listening at: {self.host}:{self.port}")
        uvicorn.run(app, host=self.host, port=self.port)
