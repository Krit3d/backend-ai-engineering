from pydantic import EmailStr
import sqlite3


def create_table() -> None:
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY, 
                username TEXT,
                age INTEGER,
                email TEXT UNIQUE
            )
        """
        )


def add_user(username: str, age: int, email: EmailStr) -> None:
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO users (username, age, email) VALUES (?, ?, ?)
            """,
            (username, age, email),
        )
        con.commit()


def get_email_list() -> tuple[str]:
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        cur.execute("SELECT email FROM users")

        return cur.fetchall()


def get_user_id(email: EmailStr) -> tuple[int]:
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))

        return cur.fetchone()


def get_all_users() -> list[dict]:
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()

        cur.execute("SELECT * FROM users")
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        return [dict(zip(columns, row)) for row in results]
