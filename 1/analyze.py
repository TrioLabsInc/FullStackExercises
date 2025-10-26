import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("exercise.sqlite")


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    session_cursor = conn.cursor()
    lookup_cursor = conn.cursor()
    group_cursor = conn.cursor()

    counts = []

    total_sessions = session_cursor.execute(
        "SELECT COUNT(*) FROM sessions"
    ).fetchone()[0]
    print(f"total sessions: {total_sessions}")

    for i in range(1, total_sessions + 1):
        user_a_id, user_b_id = session_cursor.execute(
            f"SELECT user_a_id, user_b_id FROM sessions WHERE id = {i}"
        ).fetchone()
        group_a_id = lookup_cursor.execute(
            f"SELECT group_id FROM users WHERE id = {user_a_id}"
        ).fetchone()[0]
        group_b_id = lookup_cursor.execute(
            f"SELECT group_id FROM users WHERE id = {user_b_id}"
        ).fetchone()[0]
        pair = sorted((group_a_id, group_b_id))
        existing = None
        for entry in counts:
            if entry[0] == pair[0] and entry[1] == pair[1]:
                existing = entry
                break
        if existing is None:
            counts.append([pair[0], pair[1], 1])
        else:
            existing[2] += 1

    group_names = {
        group_id: name
        for group_id, name in group_cursor.execute('SELECT id, name FROM "group"')
    }

    for group_a_id, group_b_id, count in sorted(counts, key=lambda entry: (entry[0], entry[1])):
        name_a = group_names[group_a_id]
        name_b = group_names[group_b_id]
        print(f"{name_a} vs {name_b}: {count}")

    conn.close()


if __name__ == "__main__":
    main()
