from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from fastapi import Depends

from app.db import Base
from app.deps import get_db

class User(SQLAlchemyBaseUserTable, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pass


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)