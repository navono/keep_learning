from piccolo.conf.apps import AppRegistry
from pid_project_extract.settings import settings
from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine(path=str(settings.db_file))


APP_REGISTRY = AppRegistry(
    apps=["pid_project_extract.db.app_conf"]
)
