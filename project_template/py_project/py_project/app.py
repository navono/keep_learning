import asyncio
from py_project.utils import Config, CustomizeLogger
from py_project.http import HTTPServer

CONTEXT_SETTINGS = dict(auto_envvar_prefix="ASSISTANTS")

gen_config = Config().get_config()
logger = CustomizeLogger.make_logger(gen_config['log'])


async def start():
    http_server = HTTPServer(gen_config['http'])
    http_task = asyncio.create_task(http_server.start())

    tasks = [
        http_task
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"task failed with exception: {result}")
