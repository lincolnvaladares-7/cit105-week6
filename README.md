# CIT 105 Week 6 — SQLite Kanban

## Schema
- `boards`: one row per Kanban board, with a nonempty name.
- `cards`: cards belonging to a board through `board_id` foreign key; nonempty title; constrained `priority` and `status`.
- Foreign key enforcement is enabled on every connection.

## Run
```bash
pip install -r requirements.txt
python init_db.py
streamlit run app.py
```

## Tests
```bash
pytest -q
```

## JSON migration
Commit and back up your original JSON first. If it has the format `{"cards": [{"id": 1, "title": "Example", "description": "", "priority": "medium", "status": "todo"}]}`, run:
```bash
python migrate_json.py cards.json
```
This is a **new reference app**, not proof of migration from the previous Week 6 application. The existing JSON and original storage interface were unavailable.

## Manual retest checklist
- [ ] Create a card
- [ ] Edit card title, description, priority
- [ ] Move through To Do → Doing → Done
- [ ] Restart app and verify persistence
- [ ] Delete card
- [ ] Test AI task breakdown (not implemented in this reference app)

Do not mark items complete until personally verified.
