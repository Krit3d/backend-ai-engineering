from fastapi import APIRouter, HTTPException
from ..database import add_user, get_all_users, get_user
from ..schemas.users import UserCreate, User

# Organizing user-related endpoints
router = APIRouter()


@router.get("/api/users")
async def get_users_data() -> list[User]:
    raw_users = await get_all_users()

    # We can pass dict to a 'User' by turning on `from_attributes` property
    return [User(**u) for u in raw_users]


# POST endpoint for user registration
@router.post("/api/users", response_model=User)
async def create_user(user: UserCreate) -> User:
    try:
        user_id = await add_user(user.username, user.age, user.email)
    except ValueError:
        # Get a specific 409 status code instead of internal 500 error
        raise HTTPException(status_code=409, detail="User already exists!")
    else:
        # model_dump is for creation of model instances from obj with attrs
        return User(id=user_id, **user.model_dump())


@router.get("/api/users/{user_id}")
async def get_user_data(user_id: int) -> User:
    raw_user = await get_user(user_id)

    if raw_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**raw_user)
