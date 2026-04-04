from fastapi import APIRouter, HTTPException
from ..database import add_user, get_user, get_all_users
from ..schemas.users import UserCreate, User

router = APIRouter()


@router.post("/api/users")
async def create_user(user: UserCreate) -> dict:
    try:
        user_id = await add_user(user.username, user.age, user.email)
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists!")
    else:
        return User(id=user_id, **user.model_dump())


@router.get("/api/users")
async def get_users_data() -> list[User]:
    raw_users = await get_all_users()

    return [User(**u) for u in raw_users]


@router.get("/api/users/{user_id}")
async def get_user_data(user_id: int) -> User:
    raw_user = await get_user(user_id)
    if raw_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**raw_user)
