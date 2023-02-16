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

# import string
# import random
# from fastapi.encoders import jsonable_encoder

# from app import models
# from app import schemas
# from app import crud

# def random_lower_string(k=32) -> str:
#     return "".join(random.choices(string.ascii_lowercase, k=k))

# @pytest.fixture()
# def food(db):
#     brand = random_lower_string()
#     name = random_lower_string()
#     food_dict = schemas.FoodCreate(brand= brand, name= name)

#     food = crud.create(obj_in=food_dict, db=db, model=models.Food)
#     # food = schemas.Food(food)
#     food = schemas.Food(**jsonable_encoder(food))
#     return jsonable_encoder(food)

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