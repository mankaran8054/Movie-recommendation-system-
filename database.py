import sqlite3
from datetime import datetime


DATABASE = "movie_recommender.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            movie_title TEXT NOT NULL,
            viewed_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            movie_title TEXT NOT NULL,
            added_at TEXT NOT NULL,
            UNIQUE(user_id, movie_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def get_or_create_user(name, email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    if user:
        connection.close()
        return user

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO users
        (name, email, created_at)
        VALUES (?, ?, ?)
        """,
        (
            name,
            email,
            created_at
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return (
        user_id,
        name,
        email
    )


def add_history(user_id, movie_id, movie_title):
    connection = get_connection()
    cursor = connection.cursor()

    viewed_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO history
        (user_id, movie_id, movie_title, viewed_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            movie_id,
            movie_title,
            viewed_at
        )
    )

    connection.commit()
    connection.close()


def get_history(user_id, limit=None):
    connection = get_connection()
    cursor = connection.cursor()

    if limit is not None:

        cursor.execute(
            """
            SELECT movie_id, movie_title, viewed_at
            FROM history
            WHERE user_id = ?
            ORDER BY viewed_at DESC
            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        )

    else:

        cursor.execute(
            """
            SELECT movie_id, movie_title, viewed_at
            FROM history
            WHERE user_id = ?
            ORDER BY viewed_at DESC
            """,
            (user_id,)
        )

    history = cursor.fetchall()

    connection.close()

    return history


def get_unique_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT movie_id, movie_title
        FROM history
        WHERE user_id = ?
        GROUP BY movie_id
        ORDER BY MAX(viewed_at) DESC
        """,
        (user_id,)
    )

    history = cursor.fetchall()

    connection.close()

    return history


def add_favorite(user_id, movie_id, movie_title):
    connection = get_connection()
    cursor = connection.cursor()

    added_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO favorites
        (user_id, movie_id, movie_title, added_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            movie_id,
            movie_title,
            added_at
        )
    )

    connection.commit()
    connection.close()


def remove_favorite(user_id, movie_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM favorites
        WHERE user_id = ? AND movie_id = ?
        """,
        (
            user_id,
            movie_id
        )
    )

    connection.commit()
    connection.close()


def is_favorite(user_id, movie_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM favorites
        WHERE user_id = ? AND movie_id = ?
        """,
        (
            user_id,
            movie_id
        )
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def get_favorites(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT movie_id, movie_title, added_at
        FROM favorites
        WHERE user_id = ?
        ORDER BY added_at DESC
        """,
        (user_id,)
    )

    favorites = cursor.fetchall()

    connection.close()

    return favorites


def get_user_stats(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM history
        WHERE user_id = ?
        """,
        (user_id,)
    )

    watched_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM favorites
        WHERE user_id = ?
        """,
        (user_id,)  
    )

    favorite_count = cursor.fetchone()[0]

    connection.close()

    return watched_count, favorite_count