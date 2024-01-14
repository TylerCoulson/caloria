import random
import string
import pytest
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from app.auth.db import User
from datetime import date, timedelta, datetime
from app.api.calcs.calorie_calcs import PersonsDay


def read_data_from_file() -> dict:
    with open("app/tests/test_data/user_data.sql", "r") as f:
        user_data = f.read()
    with open("app/tests/test_data/profile_data.sql", "r") as f:
        profiles_data = f.read()
    with open("app/tests/test_data/food_categories.sql", "r") as f:
        food_categories = f.read()
    with open("app/tests/test_data/food_data.sql", "r") as f:
        food_data = f.read()
    with open("app/tests/test_data/servings_data.sql", "r") as f:
        serving_data = f.read()
    with open("app/tests/test_data/food_log_data.sql", "r") as f:
        food_log_data = f.read()

    return {"user_data": user_data, "profiles_data": profiles_data, "food_categories": food_categories, "food_data": food_data, "serving_data": serving_data, "food_log_data": food_log_data}

async def add_data_to_db(data: dict, session: Session):
    for sql in data.values():
        await session.execute(text(sql))
    return session

def random_lower_string(k=32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_date(start: date = date(1923, 1, 1), end: date = date(2010, 12, 31)) -> date:
    days_difference = end - start
    random_date = start + timedelta(days=days_difference.days) * random.random()

    return random_date

@pytest.fixture()
async def user(db):
    user_create = User(email=f"{random_lower_string()}@example.com", hashed_password="string")
    db.add(user_create)
    await db.commit()
    await db.refresh(user_create)
    return user_create

@pytest.fixture(scope="module")
async def module_user(db):
    user_create = User(email=f"{random_lower_string()}@example.com", hashed_password="string")
    db.add(user_create)
    await db.commit()
    await db.refresh(user_create)
    return jsonable_encoder(user_create)

@pytest.fixture(scope="module")
async def module_profile(db, module_user) -> models.Profile:
    profile = {"id": 1, "start_date": "2022-12-06", "start_weight": 322.4, "goal_weight": 150.0, "sex": 'Male', "birthdate": "1992-12-05", "height": 70, "lbs_per_week": 2.0, "activity_level": 2.0, "user_id": 1}
    
    return profile