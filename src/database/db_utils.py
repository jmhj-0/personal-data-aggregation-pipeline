import psycopg2
import os
import logging
import pandas as pd
from typing import Optional, List, Dict, Any
from config.config import DB_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    """Get a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['name'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def create_tables():
    """Create tables from schema.sql."""
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(schema_sql)
                conn.commit()
        logger.info("Tables created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating tables: {e}")
        raise

def insert_data(table: str, data: List[Dict[str, Any]]):
    """Insert data into a table."""
    if not data:
        return

    columns = list(data[0].keys())
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

    values = [tuple(row[col] for col in columns) for row in data]

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, values)
                conn.commit()
        logger.info(f"Inserted {len(data)} rows into {table}.")
    except psycopg2.Error as e:
        logger.error(f"Error inserting data into {table}: {e}")
        raise

def fetch_data(table: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch data from a table."""
    query = f"SELECT * FROM {table}"
    if limit:
        query += f" LIMIT {limit}"

    try:
        with get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        return df.to_dict('records')
    except psycopg2.Error as e:
        logger.error(f"Error fetching data from {table}: {e}")
        raise