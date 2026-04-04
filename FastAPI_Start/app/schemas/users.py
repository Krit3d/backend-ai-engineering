from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    age: int
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
