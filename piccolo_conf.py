from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from core.settings import settings

DB = PostgresEngine(
    config={
        "user": settings.db_user,
        "password": settings.db_password,
        "host": settings.db_host,
        "database": settings.db_name,
        "port": settings.db_port,
    }
)

APP_REGISTRY = AppRegistry(apps=["apps.auth.piccolo_app"])
