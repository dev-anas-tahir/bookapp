from environs import Env
from piccolo.engine import PostgresEngine

env = Env()
env.read_env(".env.dev")

DB = PostgresEngine(
    config={
        "user": env("DB_USER"),
        "password": env("DB_PASSWORD"),
        "host": env("DB_HOST"),
        "database": env("DB_NAME"),
        "port": env.int("DB_PORT"),
    }
)
