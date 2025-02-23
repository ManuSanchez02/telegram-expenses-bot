"""Database module for managing the database connection.

This module provides a singleton class to manage the database connection. It uses SQLAlchemy to
connect to a PostgreSQL database.

Example usage:

    from coin_processing.db import Database

    database_url = "postgresql://user:password@localhost/db"
    Database.initialize(database_url)

    with Database.get_session() as session:
        session.execute("SELECT 1")
"""

import os
from asyncio import current_task

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


def build_postgres_url(user: str, password: str, db: str, host: str) -> str:
    """
    Build a PostgreSQL URL from the given parameters.

    Args:
    - user: The username to connect to the database.
    - password: The password to connect to the database.
    - db: The name of the database.
    - host: The host of the database.

    Returns:
        postgres_url: The database URL in the format: "postgresql://[user]:[password]@[host]/[db]"
    """
    return f"postgresql://{user}:{password}@{host}/{db}"


def get_database_url() -> str:
    """
    Form a PostgreSQL URL from the environment variables.

    Expected environment variables:
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - POSTGRES_DB
    - POSTGRES_HOST

    Returns:
        postgres_url: The database URL in the format: \
        "postgresql://[POSTGRES_USER]:[POSTGRES_PASSWORD]@[POSTGRES_HOST]/[POSTGRES_DB]"

    Raises:
        ValueError: If any of the required environment variables are not set.
    """

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")

    if not POSTGRES_USER:
        raise ValueError("POSTGRES_USER environment variable not set.")
    if not POSTGRES_PASSWORD:
        raise ValueError("POSTGRES_PASSWORD environment variable not set.")
    if not POSTGRES_DB:
        raise ValueError("POSTGRES_DB environment variable not set.")
    if not POSTGRES_HOST:
        raise ValueError("POSTGRES_HOST environment variable not set.")

    return build_postgres_url(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST)


class _DatabaseMeta(type):
    """Singleton metaclass for the Database class."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Ensure that only one instance of the class is created."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=_DatabaseMeta):
    """Singleton class for managing the database connection.

    This class follows the Singleton design pattern to ensure that only one
    instance of the class is created.

    **Warning**: This class is not thread-safe.
    """

    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, database_url):
        """Initialize the database connection using the provided URL.

        Args:
            database_url: The URL to connect to the database. It must be a valid database URL.

        Raises:
            SQLAlchemyError: An error ocurred while trying to connect to the database.

        """
        if cls._engine is None:
            print(current_task())
            cls._engine = create_async_engine(database_url)
            cls._session_factory = async_scoped_session(
                async_sessionmaker(cls._engine),
                scopefunc=current_task,
            )

    @classmethod
    async def test_connection(cls):
        """Test the connection to the database.

        The database must be initialized before calling this method.

        Returns:
            connected: A boolean indicating if the connection was successful.
        """
        if cls._engine is None:
            return False

        try:
            async with cls.get_session() as session:
                await session.execute(text("SELECT 1"))
        except (ConnectionError, SQLAlchemyError):
            return False
        return True

    @classmethod
    async def get_session(cls) -> AsyncSession:
        """Get a new session from the session factory.

        Returns:
            session: A new session instance.

        Raises:
            ConnectionError: If the database is not initialized.
        """
        if cls._session_factory is None:
            raise ConnectionError("Database is not initialized. Call initialize() first.")
        return cls._session_factory()
