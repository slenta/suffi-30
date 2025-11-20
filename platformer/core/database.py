"""Database connection and initialization for Vercel Postgres."""

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Manages PostgreSQL database connections and operations."""

    _connection_pool = None

    @classmethod
    def initialize_pool(cls):
        """Initialize the connection pool."""
        if cls._connection_pool is None:
            database_url = os.getenv("POSTGRES_URL")
            if not database_url:
                raise ValueError(
                    "POSTGRES_URL environment variable not set. "
                    "Please configure your database connection."
                )

            try:
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn=1, maxconn=10, dsn=database_url
                )
            except Exception as e:
                raise Exception(f"Failed to create connection pool: {e}")

    @classmethod
    def get_connection(cls):
        """Get a connection from the pool."""
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        """Return a connection to the pool."""
        if cls._connection_pool:
            cls._connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool."""
        if cls._connection_pool:
            cls._connection_pool.closeall()
            cls._connection_pool = None


def create_highscores_table():
    """Create the highscores table if it doesn't exist."""
    connection = None
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Create table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS highscores (
                id SERIAL PRIMARY KEY,
                level_name VARCHAR(255) NOT NULL,
                player_name VARCHAR(255) NOT NULL,
                total_score INTEGER NOT NULL,
                time_score INTEGER NOT NULL,
                trophy_score INTEGER NOT NULL,
                damage_score INTEGER NOT NULL,
                life_score INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        # Create index for faster queries
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_level_score 
            ON highscores(level_name, total_score DESC);
        """
        )

        connection.commit()
        cursor.close()
        print("✅ Highscores table created successfully")

    except Exception as e:
        print(f"⚠️ Error creating highscores table: {e}")
        if connection:
            connection.rollback()
        raise

    finally:
        if connection:
            DatabaseConnection.return_connection(connection)


def is_postgres_available():
    """Check if PostgreSQL connection is available."""
    try:
        database_url = os.getenv("POSTGRES_URL")
        if not database_url:
            return False

        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        DatabaseConnection.return_connection(connection)
        return True

    except Exception:
        return False
