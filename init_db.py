
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "kanban.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)

        connection.execute(
            "INSERT OR IGNORE INTO boards (id, name) VALUES (?, ?)",
            (1, "My Kanban Board")
        )

        connection.commit()

    print(f"Database initialized: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()
