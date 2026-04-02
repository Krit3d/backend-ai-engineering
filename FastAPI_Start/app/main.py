from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_table
from .routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)


@app.get("/")
async def root() -> dict:
    return {"status": "Ed is in prod"}
