from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mapper_registry = registry()
Base = mapper_registry.generate_base()

