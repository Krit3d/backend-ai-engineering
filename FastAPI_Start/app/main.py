from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_table
from .routers import users


# Application lifecycle control
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create table in database before the app starts
    await create_table()
    yield


# Passing lifespan when creating the app
app = FastAPI(lifespan=lifespan)

# Getting access to endpoints from routers
app.include_router(users.router)


# Method for basic URL
@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "Ed is in prod"}
