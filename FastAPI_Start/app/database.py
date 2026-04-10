from pydantic import EmailStr
import asyncpg

db_pool: asyncpg.Pool | None = None

# Set pool once during app startup
def set_db_pool(pool: asyncpg.Pool) -> None:
    global db_pool
    db_pool = pool

# Return initialized pool or fail fast
def _require_pool() -> asyncpg.Pool:
    if db_pool is None:
        raise RuntimeError("Database pool is not initialized")
    return db_pool


async def create_table() -> None:
    pool = _require_pool()

    async with pool.acquire() as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                username TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
            """
        )


async def add_user(username: str, age: int, email: EmailStr) -> int:
    try:
        pool = _require_pool()

        async with pool.acquire() as con:
            result = await con.fetchrow(
                """
                INSERT INTO users (username, age, email)
                VALUES ($1, $2, $3)
                RETURNING id
                """,
                username,
                age,
                email,
            )
            if result is not None:
                return result["id"]

    except asyncpg.UniqueViolationError:
        # Duplicate email (unique constraint)
        raise ValueError

    except Exception:
        # Optionally, re-raise or log for other errors
        raise


async def get_user(user_id: int) -> asyncpg.Record | None:
    pool = _require_pool()

    async with pool.acquire() as con:
        row = await con.fetchrow(
            "SELECT id, username, age, email FROM users WHERE id = $1",
            user_id,
        )

        return row if row else None


async def get_all_users() -> list[asyncpg.Record]:
    pool = _require_pool()

    async with pool.acquire() as con:
        rows = await con.fetch("SELECT * FROM users")

        return rows
