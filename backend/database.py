import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

POOL = ConnectionPool(
    conninfo=(
        f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} "
        f"user={DB_USER} password={DB_PASSWORD}"
    ),
    min_size=1,
    max_size=10,
    open=True
)

def get_connection():
    return POOL.connection()

if __name__ == "__main__":
    with get_connection() as conn:
        print("PostgreSQL baglantisi basarili.")