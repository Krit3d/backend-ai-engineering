from contextlib import asynccontextmanager
from fastapi import FastAPI

from .config import settings
from .database import create_table, set_db_pool
from .routers import users

import asyncpg


# Application lifecycle control
@asynccontextmanager
async def lifespan(app: FastAPI):
    db_pool = await asyncpg.create_pool(dsn=settings.get_db_url())
    set_db_pool(db_pool)

    await create_table()
    yield

    await db_pool.close()


# Passing lifespan when creating the app
app = FastAPI(lifespan=lifespan)

# Getting access to endpoints from routers
app.include_router(users.router)


# Method for basic URL
@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "Ed is in prod"}
