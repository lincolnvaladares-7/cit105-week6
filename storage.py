import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).with_name('kanban.db')

@contextmanager
def connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db(db_path=DB_PATH):
    schema = Path(__file__).with_name('schema.sql').read_text(encoding='utf-8')
    with connection(db_path) as conn:
        conn.executescript(schema)
        conn.execute('INSERT OR IGNORE INTO boards(id,name) VALUES(?,?)', (1,'My Kanban Board'))

def list_cards(db_path=DB_PATH):
    with connection(db_path) as conn:
        return [dict(r) for r in conn.execute('SELECT * FROM cards WHERE board_id=? ORDER BY id', (1,))]

def add_card(title, description='', priority='medium', status='todo', db_path=DB_PATH):
    with connection(db_path) as conn:
        cur=conn.execute('INSERT INTO cards(board_id,title,description,priority,status) VALUES(?,?,?,?,?)', (1,title,description,priority,status))
        return cur.lastrowid

def update_card(card_id, title, description, priority, status, db_path=DB_PATH):
    with connection(db_path) as conn:
        return conn.execute('UPDATE cards SET title=?,description=?,priority=?,status=? WHERE id=? AND board_id=?', (title,description,priority,status,card_id,1)).rowcount

def delete_card(card_id, db_path=DB_PATH):
    with connection(db_path) as conn:
        return conn.execute('DELETE FROM cards WHERE id=? AND board_id=?', (card_id,1)).rowcount
