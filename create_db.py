import sqlite3

DB_NAME = 'url_shortener.db'


def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_url TEXT UNIQUE NOT NULL,
                long_url TEXT NOT NULL
            )
        """)
    print("Database and table created successfully!")


create_database()
