from piccolo.engine import PostgresEngine
from environs import Env

env = Env()
env.read_env(".env.dev")

DB = PostgresEngine(
    config={
        "user": env("user"),
        "password": env("password"),
        "host": env("host"),
        "database": env("database"),
        "port": env.int("port"),
    }
)
