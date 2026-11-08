"""Utilities for connecting to the NBA SQLite database."""

import sqlite3
from pathlib import Path
from typing import Any
import pandas as pd


def get_database_path() -> Path:
    """Locate the NBA SQLite database."""

    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"

    # Prefer the expected database filename.
    preferred_path = data_dir / "nba.sqlite"

    if preferred_path.is_file():
        return preferred_path

    # Otherwise, search for a supported database file.
    supported_extensions = {".sqlite", ".sqlite3", ".db"}

    candidates = [
        path
        for path in data_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in supported_extensions
    ]

    if len(candidates) == 0:
        raise FileNotFoundError(f"No SQLite database found in {data_dir}")

    if len(candidates) > 1:
        raise RuntimeError(f"Multiple databases found: {candidates}")

    return candidates[0]


def get_connection(
    database_path: str | Path | None = None,
) -> sqlite3.Connection:
    """Create a connection to the NBA database."""

    if database_path is None:
        database_path = get_database_path()

    database_path = Path(database_path)

    if not database_path.is_file():
        raise FileNotFoundError(f"Database does not exist: {database_path}")

    return sqlite3.connect(str(database_path))


def read_sql_query(
    query: str,
    params: tuple[Any, ...] | dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Execute a SQL query and return a pandas DataFrame."""

    connection = get_connection()

    try:
        result = pd.read_sql_query(
            query,
            connection,
            params=params,
        )
    finally:
        connection.close()

    return result
