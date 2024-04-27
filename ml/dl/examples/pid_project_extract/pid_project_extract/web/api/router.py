from fastapi.routing import APIRouter
from pid_project_extract.web.api import monitoring
from pid_project_extract.web.api import img_process
from pid_project_extract.web.api import utils

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(img_process.router)
api_router.include_router(utils.router)

