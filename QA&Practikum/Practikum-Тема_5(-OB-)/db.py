import sqlite3
from note import Note

DB_NAME = "notes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def add_note(note: Note):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)',
    (note.title, note.content, note.created_at.isoformat()))
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM notes ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [Note.from_row(row) for row in rows]

def delete_note(note_id: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()

def update_note(note_id:int, title:str, content:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE notes SET title=?, content=? WHERE id=?', (title, content, note_id,))
    conn.commit()
    conn.close()
