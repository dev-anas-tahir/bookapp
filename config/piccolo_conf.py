from environs import Env
from piccolo.engine import PostgresEngine

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
