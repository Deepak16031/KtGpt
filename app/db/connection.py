import psycopg2
from psycopg2.extras import DictCursor
import urllib.parse
from config import SUPABASE_DBNAME, SUPABASE_HOST, SUPABASE_PASSWORD, SUPABASE_PORT, SUPABASE_USER


def get_connection():
    """Create and return a database connection to Supabase PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname=SUPABASE_DBNAME,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise


def get_dict_cursor(conn):
    """Create and return a dictionary cursor"""
    return conn.cursor(cursor_factory=DictCursor)
