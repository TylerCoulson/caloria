import random
import string
import pytest
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
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

def create_random_profile_dict() -> dict:
    start_date = date(2022,12,6)
    password_hash = random_lower_string()
    email = f"{random_lower_string()}@{random_lower_string(6)}.com"
    start_weight = random.randint(200, 700) + round(random.random(), 2)
    goal_weight = random.randint(100, 180) + round(random.random(), 2)
    sex = random.choice(["male", "female"])
    birthdate = random_date()
    height = random.randint(48, 84)
    lbs_per_week = round(random.random() * 2)
    activity_level = random.choice([1.2, 1.375, 1.55, 1.725, 1.9])

    profile_dict = schemas.ProfileCreate(
        start_date=start_date,
        password_hash=password_hash,
        email=email,
        start_weight=start_weight,
        goal_weight=goal_weight,
        sex=sex,
        birthdate=birthdate,
        height=height,
        lbs_per_week=lbs_per_week,
        activity_level=activity_level,
    )

    return jsonable_encoder(profile_dict)


@pytest.fixture()
async def profile(db, user) -> models.Profile:
    data = schemas.ProfileCreate(
        start_date=date(2022,12,6),
        password_hash=random_lower_string(),
        email=f"{random_lower_string()}@{random_lower_string(6)}.com",
        start_weight=322.4,
        goal_weight=150,
        sex='male',
        birthdate=date(1992,12,5),
        height=70,
        lbs_per_week=2,
        activity_level=1.2,
        user_id=user.id
    )
    profile = await crud.create(obj_in=data, db=db, model=models.Profile)
    
    return jsonable_encoder(profile)


@pytest.fixture()
async def food(db) -> models.Food:
    brand = random_lower_string()
    name = random_lower_string()
    food_dict = schemas.FoodCreate(brand= brand, name= name)

    food = await crud.create(obj_in=food_dict, db=db, model=models.Food)
    food = jsonable_encoder(food)
    return food


@pytest.fixture()
async def food_2(db):
    brand = random_lower_string()
    name = random_lower_string()
    food_dict = schemas.FoodCreate(brand= brand, name= name)

    food = await crud.create(obj_in=food_dict, db=db, model=models.Food)
    food = jsonable_encoder(food)
    return food


@pytest.fixture()
async def profile(db, user) -> models.Profile:
    data = schemas.ProfileCreate(
        start_date=date(2022,12,6),
        password_hash=random_lower_string(),
        email=f"{random_lower_string()}@{random_lower_string(6)}.com",
        start_weight=322.4,
        goal_weight=150,
        sex='male',
        birthdate=date(1992,12,5),
        height=70,
        lbs_per_week=2,
        activity_level=1.2,
        user_id=user.id
    )
    profile = await crud.create(obj_in=data, db=db, model=models.Profile)
    
    return jsonable_encoder(profile)

@pytest.fixture()
async def serving(food, db) -> models.ServingSize:
    data = schemas.ServingSizeCreate(
        food_id=food['id'],
        description=random_lower_string(),
        calories=500,
        fats=40,
        carbs=10,
        protein=20,
    )

    serving = await crud.create(obj_in=data, db=db, model=models.ServingSize)  
    return jsonable_encoder(serving)


@pytest.fixture()
async def food_log(
    module_profile, food, serving, db
):
    profile_id = module_profile['id']
    food_id = food['id']
    serving_size_id = serving['id']
    serving_amount = 1
    
    data = {
        "date": module_profile['start_date'],
        "food_id": food_id,
        "serving_size_id": serving_size_id,
        "serving_amount": serving_amount,
        "profile_id": profile_id,
    }

    data = schemas.FoodLogCreate(**data)
    log = await crud.create(obj_in=data, db=db, model=models.Food_Log)
    return jsonable_encoder(log)

@pytest.fixture()
async def food_log_2(
    module_profile, food, serving, db
):
    profile_id = module_profile['id']
    food_id = food['id']
    serving_size_id = serving['id']
    serving_amount = 1
    
    data = {
        "date": datetime.strptime(module_profile['start_date'], "%Y-%m-%d") + timedelta(1),
        "food_id": food_id,
        "serving_size_id": serving_size_id,
        "serving_amount": serving_amount,
        "profile_id": profile_id,
    }

    data = schemas.FoodLogCreate(**data)
    log = await crud.create(obj_in=data, db=db, model=models.Food_Log)
    return jsonable_encoder(log)

@pytest.fixture()
async def daily_output(food_log:models.Food_Log): 
    food_log['date'] = date(2022,12,7)
    food_log = schemas.FoodLog(**food_log)
    return PersonsDay(
        height = 70,
        start_weight = 322.4,
        start_date = date(2022,12,6),
        lbs_per_day = 2/7,
        birthdate = date(1992,12,5),
        sex = 'male',
        activity_level = 1.2,
        goal_weight = 150,
        profile_logs = [food_log],
    )

from app.auth.db import User
from .utils import random_lower_string

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
    profile = {"id": 1, "start_date": '2023-04-09', "start_weight": 803.3, "goal_weight": 241.0, "sex": 'Male', "birthdate": '1994-10-26', "height": 10, "lbs_per_week": 1.38, "activity_level": 1.8, "user_id": 1}
    # data = schemas.ProfileCreate(**profile)
    
    return profile