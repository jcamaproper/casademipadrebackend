import psycopg2
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get PostgreSQL connection details from environment variables
PG_USER = os.getenv("PGUSER")
PG_PASSWORD = os.getenv("PGPASSWORD")
PG_HOST = os.getenv("PGHOST")
PG_PORT = os.getenv("PGPORT")
PG_DATABASE = os.getenv("PGDATABASE")

# Database connection setup
conn = psycopg2.connect(
    dbname=PG_DATABASE,
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT
)

@contextmanager
def get_db_cursor():
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

