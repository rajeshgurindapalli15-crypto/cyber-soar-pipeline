import os
import sqlite3
import pytest
from engine.soar_logger import init_sqlite, SQLITE_DB
def test_sqlite_initialization():
    """Verify local SQLite audit database and schema initialization."""
    if os.path.exists(SQLITE_DB):
        os.remove(SQLITE_DB)
    
    init_sqlite()
    assert os.path.exists(SQLITE_DB), "SQLite database file should be created."

    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs';")
    table_exists = cursor.fetchone()
    conn.close()

    assert table_exists is not None, "audit_logs table must exist in the schema."