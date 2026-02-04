from piccolo.engine import PostgresEngine

DB = PostgresEngine(
    config={
        "user": "piccolo",
        "password": "piccolo",
        "host": "localhost",
        "database": "bookapp",
        "port": 5432,
    }
)
