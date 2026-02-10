import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "cctv_db"),
    "user": os.getenv("DB_USER", "cctv_user"),
    "password": os.getenv("DB_PASSWORD", "cctv_password")
}

def get_db_connection():
    """Create and return a new database connection"""
    return psycopg2.connect(**DB_CONFIG)
