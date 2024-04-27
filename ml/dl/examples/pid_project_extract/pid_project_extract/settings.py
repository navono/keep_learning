import os
import enum
from pathlib import Path
from tempfile import gettempdir
from typing import List, Optional
from pydantic import BaseSettings

from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # Application host and port
    host: str = "127.0.0.1"
    port: int = int(os.environ.get("PID_PROJECT_EXTRACT_PORT")) if os.environ.get(
        "PID_PROJECT_EXTRACT_PORT") else 8000

    # quantity of workers for uvicorn
    workers_count: int = 1

    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_file: Path = TEMP_DIR / "db.sqlite3"
    db_echo: bool = False

    pid_dir: str = os.environ.get("PID_PROJECT_EXTRACT_PID_DIR")

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="sqlite",
            path=f"///{self.db_file}"
        )

    class Config:
        env_file = ".env_dev"
        env_prefix = "PID_PROJECT_EXTRACT_"
        env_file_encoding = "utf-8"


settings = Settings(_env_file=Settings.Config.env_file)
