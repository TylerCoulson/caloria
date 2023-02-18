from typing import Generator

import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine  # type:ignore
from sqlalchemy.orm import sessionmaker  # type:ignore
from app.db import Base  # type:ignore
from app.config import settings
from app.main import app
from app.deps import get_db
from app.tests.utils import *

engine = create_engine(
    settings.SQLALCHEMY_TEST_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    # setup
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    # teardown
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c