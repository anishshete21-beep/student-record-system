import sqlite3
import os

DATABASE_FOLDER = "database"
DATABASE_FILE = "students.db"

os.makedirs(DATABASE_FOLDER, exist_ok=True)

DATABASE_PATH = os.path.join(DATABASE_FOLDER, DATABASE_FILE)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def execute_query(query, values=()):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(query, values)

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def fetch_all(query, values=()):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query, values)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def fetch_one(query, values=()):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query, values)

    row = cursor.fetchone()

    connection.close()

    if row:
        return dict(row)

    return None


create_database()