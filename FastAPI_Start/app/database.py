from pydantic import EmailStr
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


async def get_all_users() -> list[dict]:
    async with aiosqlite.connect("users.db") as con:
        async with con.execute("SELECT * FROM users") as cur:
            columns = [desc[0] for desc in cur.description]
            results = await cur.fetchall()

            return [dict(zip(columns, row)) for row in results]
