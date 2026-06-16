import sqlite3
import bcrypt

DB_FILE = "vault.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master (
            id INTEGER PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()

def is_master_set():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM master")
    result = cursor.fetchone()
    conn.close()
    return result is not None

def set_master_password(plain_password):
    hashed = bcrypt.hashpw(
        plain_password.encode(),
        bcrypt.gensalt()
    ).decode()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO master (password_hash) VALUES (?)",
        (hashed,)
    )

    conn.commit()
    conn.close()

def verify_master_password(plain_password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM master")
    result = cursor.fetchone()

    conn.close()

    if result:
        return bcrypt.checkpw(
            plain_password.encode(),
            result[0].encode()
        )

    return False

def add_entry(site, username, password, notes=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vault
        (site, username, password, notes)
        VALUES (?, ?, ?, ?)
        """,
        (site, username, password, notes)
    )

    conn.commit()
    conn.close()

def get_all_entries():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, site, username, password, notes FROM vault"
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_entry(entry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM vault WHERE id=?",
        (entry_id,)
    )

    conn.commit()
    conn.close()

def update_entry(entry_id, site, username, password, notes=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE vault
        SET site=?, username=?, password=?, notes=?
        WHERE id=?
        """,
        (site, username, password, notes, entry_id)
    )

    conn.commit()
    conn.close()

def search_entries(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, site, username, password, notes
        FROM vault
        WHERE site LIKE ? OR username LIKE ?
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    rows = cursor.fetchall()

    conn.close()

    return rows