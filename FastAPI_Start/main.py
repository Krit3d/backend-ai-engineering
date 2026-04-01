from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from database import (
    create_table,
    add_user,
    get_all_users,
)


class UserCreate(BaseModel):
    username: str
    age: int
    email: EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> dict:
    return {"status": "Ed is in prod"}


@app.post("/api/users")
async def create_user(user: UserCreate) -> dict:
    try:
        user_id = await add_user(user.username, user.age, user.email)
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists!")
    else:
        return {
            "message": f"User {user.username} with id={user_id} successfully created!",
            "user": user.model_dump(),
        }


@app.get("/api/users")
async def get_users_data() -> list[dict]:
    return await get_all_users()
