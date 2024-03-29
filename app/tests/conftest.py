from typing import Generator

import pytest
from httpx import AsyncClient
from app.db import Base  # type:ignore
from app.config import settings
from app.main import app
from app.deps import get_db
from app.auth.users import get_current_profile, current_active_user
from app import models
from app.tests.utils import *
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.tests.utils import read_data_from_file, add_data_to_db

engine = create_async_engine(
    settings.SQLALCHEMY_TEST_DATABASE_URI,
    connect_args={"check_same_thread": False},
)
async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

data = read_data_from_file()

@pytest.mark.anyio
@pytest.fixture(scope="module")
async def db(anyio_backend) -> Generator:
    # setup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        await add_data_to_db(data, session)
        yield session

    # teardown
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
async def client(db, module_profile, module_user) -> Generator:
    async def override_get_db():
        try:
            yield db
        finally:
            await db.close()

    async def override_get_user():
        return models.User(**module_user)
    
    async def override_get_profile():
        return models.Profile(**module_profile)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[current_active_user] = override_get_user
    app.dependency_overrides[get_current_profile] = override_get_profile

    async with AsyncClient(app=app, base_url='http://test') as c:
        yield c



@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'