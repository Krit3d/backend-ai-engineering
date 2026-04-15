from pydantic import EmailStr

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import settings
from .models import User

engine = create_async_engine(settings.get_db_url(), echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def add_user(username: str, age: int, email: EmailStr) -> int:
    async with AsyncSessionLocal() as session:
        user = User(username=username, age=age, email=str(email))
        session.add(user)

        try:
            await session.commit()

        except IntegrityError as exc:
            await session.rollback()

            # Use exception chaining
            raise ValueError from exc

        await session.refresh(user)

        return user.id


async def get_user(user_id: int) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))

        return result.scalar_one_or_none()


async def get_all_users() -> list[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))

        return list(result.scalars().all())
