import psycopg2
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection setup should ideally be within a function or context manager
def get_database_connection():
    PG_USER = os.getenv("PGUSER")
    PG_PASSWORD = os.getenv("PGPASSWORD")
    PG_HOST = os.getenv("PGHOST")
    PG_PORT = os.getenv("PGPORT")
    PG_DATABASE = os.getenv("PGDATABASE")

    return psycopg2.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

@contextmanager
def get_db_cursor():
    conn = None
    cursor = None
    try:
        # Ensure the connection is established within the try block to handle any connection errors
        conn = get_database_connection()
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except psycopg2.InterfaceError as e:
        # Handle specific psycopg2 connection errors
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass  # If rollback fails, the connection might be broken
        raise e
    except Exception as e:
        # Handle other exceptions
        if conn is not None:
            conn.rollback()
        raise e
    finally:
        # Ensure cursor is closed if it was successfully created
        if cursor is not None:
            cursor.close()
        # Close the connection in the finally block to ensure it's always closed after the operation
        if conn is not None:
            conn.close()


