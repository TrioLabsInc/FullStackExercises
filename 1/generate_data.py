import random
import sqlite3
from pathlib import Path

USER_COUNT = 20
SESSION_COUNT = 50_000
GROUP_COUNT = 3
DB_PATH = Path(__file__).with_name("exercise.sqlite")


def seed_groups(cursor: sqlite3.Cursor) -> None:
    cursor.executemany(
        'INSERT INTO "group" (name) VALUES (?)',
        [(f"Group {idx}",) for idx in range(1, GROUP_COUNT + 1)],
    )


def seed_users(cursor: sqlite3.Cursor) -> None:
    rows = []
    for idx in range(1, USER_COUNT + 1):
        group_id = ((idx - 1) % GROUP_COUNT) + 1
        rows.append((f"User {idx}", group_id))
    cursor.executemany(
        "INSERT INTO users (name, group_id) VALUES (?, ?)",
        rows,
    )


def seed_sessions(cursor: sqlite3.Cursor) -> None:
    rows = []
    for _ in range(SESSION_COUNT):
        user_a = random.randint(1, USER_COUNT)
        user_b = random.randint(1, USER_COUNT - 1)
        if user_b >= user_a:
            user_b += 1
        rows.append((user_a, user_b))
    cursor.executemany(
        "INSERT INTO sessions (user_a_id, user_b_id) VALUES (?, ?)",
        rows,
    )


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(
        """
        DROP TABLE IF EXISTS sessions;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS "group";

        CREATE TABLE "group" (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            group_id INTEGER NOT NULL REFERENCES "group"(id)
        );

        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY,
            user_a_id INTEGER NOT NULL REFERENCES users(id),
            user_b_id INTEGER NOT NULL REFERENCES users(id)
        );
        """
    )
    seed_groups(cursor)
    seed_users(cursor)
    seed_sessions(cursor)
    conn.commit()
    conn.close()
    print(f"database written to {DB_PATH}")


if __name__ == "__main__":
    main()
