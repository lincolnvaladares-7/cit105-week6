PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS boards (id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(trim(name))>0));
CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, board_id INTEGER NOT NULL REFERENCES boards(id) ON DELETE CASCADE, title TEXT NOT NULL CHECK(length(trim(title))>0), description TEXT NOT NULL DEFAULT '', priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low','medium','high')), status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo','doing','done')));
CREATE INDEX IF NOT EXISTS idx_cards_board ON cards(board_id);
