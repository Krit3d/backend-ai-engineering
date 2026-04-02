from fastapi import APIRouter, HTTPException
from ..database import add_user, get_all_users
from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    age: int
    email: EmailStr


@router.post("/api/users")
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


@router.get("/api/users")
async def get_users_data() -> list[dict]:
    return await get_all_users()
