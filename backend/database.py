import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

_pool: ConnectionPool | None = None

def _get_pool() -> ConnectionPool:
    """Lazily creates the connection pool on first use.

    Creating it eagerly at import time (the old behavior) meant just
    *importing* this module — e.g. from a unit test that mocks the
    repositories and never actually touches the database — would still
    try to open real connections in the background. Building it lazily
    means importing the module has no side effects.
    """
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=(
                f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} "
                f"user={DB_USER} password={DB_PASSWORD}"
            ),
            min_size=1,
            max_size=10,
            open=True,
        )
    return _pool

def get_connection():
    return _get_pool().connection()

if __name__ == "__main__":
    with get_connection() as conn:
        print("PostgreSQL baglantisi basarili.")