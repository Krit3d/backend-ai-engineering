from pydantic import EmailStr
from typing import Any
import aiosqlite


async def create_table() -> None:
    async with aiosqlite.connect("users.db") as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY, 
                username TEXT,
                age INTEGER,
                email TEXT UNIQUE
            )
            """
        )
        await con.commit()


async def add_user(username: str, age: int, email: EmailStr) -> int | None:
    async with aiosqlite.connect("users.db") as con:
        try:
            cur = await con.execute(
                """
                INSERT INTO users (username, age, email) VALUES (?, ?, ?)
                """,
                (username, age, email),
            )
        except aiosqlite.IntegrityError:
            raise ValueError
        else:
            await con.commit()

            return cur.lastrowid


async def get_user(user_id: int) -> dict[str, Any] | None:
    async with aiosqlite.connect("users.db") as con:
        con.row_factory = aiosqlite.Row

        async with con.execute(
            "SELECT id, username, age, email FROM users WHERE id = ?",
            (user_id,),
        ) as cur:
            row = await cur.fetchone()

            return dict(row) if row else None


async def get_all_users() -> list[dict[str, Any]]:
    async with aiosqlite.connect("users.db") as con:
        con.row_factory = aiosqlite.Row

        async with con.execute("SELECT * FROM users") as cur:
            results = await cur.fetchall()

            return [dict(row) for row in results]
