import sqlite3
import json


DATABASE = "data/candidates.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            profile TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_candidate(profile):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO candidates
        (name, email, phone, profile)
        VALUES (?, ?, ?, ?)
        """,
        (
            profile.name,
            profile.email,
            profile.phone,
            json.dumps(profile.model_dump())
        )
    )

    connection.commit()
    connection.close()