import sqlite3
import os

# Database file path
DB_PATH = 'otopark.db'

def create_tables():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            kod INTEGER PRIMARY KEY AUTOINCREMENT,
            plaka TEXT UNIQUE,
            name TEXT,
            surname TEXT,
            tel TEXT,
            eposta TEXT,
            araç_marka TEXT,
            start_date DATE,
            finish_date DATE,
            start_clock TIME,
            false_out DATE,
            durum TEXT,
            macadres TEXT,
            passw TEXT
        )
    ''')

    # Create rights table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rights (
            kod INTEGER PRIMARY KEY AUTOINCREMENT,
            plaka TEXT,
            start_date DATE,
            finish_date DATE,
            false_out DATE,
            durum TEXT,
            odeme REAL,
            günlükfiat REAL,
            FOREIGN KEY (plaka) REFERENCES user (plaka)
        )
    ''')

    # Create usage table (for logs or usage)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "usage" (
            kod INTEGER PRIMARY KEY AUTOINCREMENT,
            alan TEXT,
            text TEXT
        )
    ''')

    # Create password table for admin
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password (
            kod INTEGER PRIMARY KEY AUTOINCREMENT,
            passw TEXT
        )
    ''')

    # Create kosullar table for terms and conditions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kosullar (
            kod INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    ''')

    # Insert default admin password if not exists
    cursor.execute("SELECT COUNT(*) FROM password")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO password (passw) VALUES (?)", ('admin123',))  # Default password

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    create_tables()