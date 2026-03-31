from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from database import (
    create_table,
    add_user,
    get_email_list,
    get_user_id,
    get_all_users,
)


class UserCreate(BaseModel):
    username: str
    age: int
    email: EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"status": "Ed is in prod"})


@app.post("/api/users")
async def create_user(user: UserCreate) -> JSONResponse:
    emails = [tup[0] for tup in get_email_list()]
    if user.email in emails:
        raise HTTPException(status_code=409, detail="User already exists!")

    add_user(user.username, user.age, user.email)

    return JSONResponse(
        content={
            "message": f"User {user.username} with id={get_user_id(user.email)[0]} successfully created!",
            "user": user.model_dump(),
        }
    )


@app.get("/api/users")
async def get_users_data() -> list[dict]:
    return get_all_users()
