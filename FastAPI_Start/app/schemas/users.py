from pydantic import BaseModel, EmailStr

# Base schema for user, containing shared attributes
class UserBase(BaseModel):
    username: str
    age: int
    email: EmailStr


class UserCreate(UserBase):
    pass

# Schema for returning user information, including the user's unique ID
class User(UserBase):
    id: int

    class Config:
        # Enables creation of model instances from objects that have attributes
        # instead of requiring dicts (useful when loading from database rows)
        from_attributes = True
