from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session_maker, SessionLocal



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()