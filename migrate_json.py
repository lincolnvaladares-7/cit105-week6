import json
import sys
from pathlib import Path
from storage import connection, init_db

def migrate(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data,dict) or not isinstance(data.get('cards'),list):
        raise ValueError('Expected JSON object with cards list')
    cards=data['cards']
    init_db()
    with connection() as conn:
        for card in cards:
            conn.execute('INSERT INTO cards(id,board_id,title,description,priority,status) VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET board_id=excluded.board_id,title=excluded.title,description=excluded.description,priority=excluded.priority,status=excluded.status', (card['id'],card.get('board_id',1),card['title'],card.get('description',''),card.get('priority','medium'),card.get('status','todo')))
    print(f'Migrated {len(cards)} cards')

if __name__ == '__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python migrate_json.py cards.json')
    migrate(sys.argv[1])
