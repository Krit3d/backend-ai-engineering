from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    age: int
    email: EmailStr


app = FastAPI()


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"status": "Ed is in prod"})


@app.post("/users")
async def create_user(user: UserCreate) -> JSONResponse:
    return JSONResponse(
        content={
            "message": f"User {user.username} successfully created!",
            "user": user.model_dump(),
        }
    )
