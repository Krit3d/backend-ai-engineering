import sqlite3


def db_start():
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, full_name TEXT)"
    )

    con.close()


def cmd_insert(user_id, full_name):
    data = (user_id, full_name)

    con = sqlite3.connect("users.db")
    cur = con.cursor()

    try:
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
            data,
        )
    except sqlite3.Error as e:
        print(f"An error occured: {type(e).__name__}.")
    finally:
        con.commit()
        con.close()


def get_all_users():
    con = sqlite3.connect("users.db")
    cursor = con.cursor()

    cursor.execute("SELECT user_id, full_name FROM users")
    users = cursor.fetchall()

    con.close()

    return users
