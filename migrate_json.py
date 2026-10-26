
import json
import sqlite3
import sys
from pathlib import Path

from init_db import DB_PATH, initialize_database


def migrate(json_path):
    path = Path(json_path)

    if not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    # Supported input:
    # {"cards": [{"id": 1, "title": "...", ...}]}
    if not isinstance(data, dict) or not isinstance(data.get("cards"), list):
        raise ValueError("Expected a JSON object containing a cards list")

    cards = data["cards"]

    # Validate before writing anything.
    for card in cards:
        if not isinstance(card, dict):
            raise ValueError("Each card must be an object")
        if not isinstance(card.get("id"), int):
            raise ValueError("Each card needs an integer id")
        if not isinstance(card.get("title"), str) or not card["title"].strip():
            raise ValueError("Each card needs a nonempty title")

    initialize_database()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        for card in cards:
            connection.execute(
                """
                INSERT INTO cards
                    (id, board_id, title, description, priority, status)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    board_id = excluded.board_id,
                    title = excluded.title,
                    description = excluded.description,
                    priority = excluded.priority,
                    status = excluded.status
                """,
                (
                    card["id"],
                    card.get("board_id", 1),
                    card["title"],
                    card.get("description", ""),
                    card.get("priority", "medium"),
                    card.get("status", "todo"),
                ),
            )

        connection.commit()

    print(f"Migrated {len(cards)} cards successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python migrate_json.py cards.json")
        sys.exit(1)

    migrate(sys.argv[1])

