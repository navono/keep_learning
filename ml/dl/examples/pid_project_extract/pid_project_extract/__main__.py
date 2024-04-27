import os
import shutil

import uvicorn
from pid_project_extract.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    os.environ['PICCOLO_CONF'] = "pid_project_extract.piccolo_conf"
    uvicorn.run(
        "pid_project_extract.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
