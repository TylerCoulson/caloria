import random
import string
import pytest
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from datetime import date, timedelta
from app.api.calcs.calorie_calcs import PersonsDay

def random_lower_string(k=32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_date(start: date = date(1923, 1, 1), end: date = date(2010, 12, 31)) -> date:
    days_difference = end - start
    random_date = start + timedelta(days=days_difference.days) * random.random()

    return random_date


def create_random_user_dict() -> dict:
    start_date = date.today()
    password_hash = random_lower_string()
    email = f"{random_lower_string()}@{random_lower_string(6)}.com"
    start_weight = random.randint(200, 700) + round(random.random(), 2)
    goal_weight = random.randint(100, 180) + round(random.random(), 2)
    sex = random.choice(["male", "female"])
    birthdate = random_date()
    height = random.randint(48, 84)
    lbs_per_week = round(random.random() * 2)
    activity_level = random.choice([1.2, 1.375, 1.55, 1.725, 1.9])

    user_dict = schemas.UserCreate(
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

    return jsonable_encoder(user_dict)

@pytest.fixture()
def user(db) -> models.User:
    # if user_dict is None:
    user_dict = create_random_user_dict()
    data = schemas.UserCreate(**user_dict)
    user = crud.create(obj_in=data, db=db, model=models.User)
    return user

@pytest.fixture()
def food(db) -> models.Food:
    brand = random_lower_string()
    name = random_lower_string()
    food_dict = schemas.FoodCreate(brand= brand, name= name)

    food = crud.create(obj_in=food_dict, db=db, model=models.Food)
    # food = schemas.Food(food)
    food = schemas.Food(**jsonable_encoder(food))
    return food

@pytest.fixture()
def food_2(db):
    brand = random_lower_string()
    name = random_lower_string()
    food_dict = schemas.FoodCreate(brand= brand, name= name)

    food = crud.create(obj_in=food_dict, db=db, model=models.Food)
    # food = schemas.Food(food)
    food = schemas.Food(**jsonable_encoder(food))
    return food

@pytest.fixture()
def serving(food, db) -> models.ServingSize:
    food_id = food.id
    data = schemas.ServingSizeCreate(
        food_id=food_id,
        description=random_lower_string(),
        calories=random.randint(1, 1000),
        fats=random.randint(1, 1000),
        carbs=random.randint(1, 1000),
        protein=random.randint(1, 1000),
    )

    serving = crud.create(obj_in=data, db=db, model=models.ServingSize)
    return serving

@pytest.fixture()
def food_log(
    user, food, serving, db
) -> models.Food_Log:
    
    user_id = user.id
    food_id = food.id
    serving_size_id = serving.id
    serving_amount = random.randint(1, 10)

    data = {
        "date": (user.start_date + timedelta(random.randint(1,100))).isoformat(),
        "food_id": food_id,
        "serving_size_id": serving_size_id,
        "serving_amount": serving_amount,
        "user_id": user_id,
    }

    data = schemas.FoodLogCreate(**data)
    log = crud.create(obj_in=data, db=db, model=models.Food_Log)
    return log

@pytest.fixture()
def daily_output(user:models.User, food_log:models.Food_Log):
    # food_log.serving_size.calories = 
    
    return PersonsDay(
        height = 70,
        start_weight = 322.4,
        start_date = date(2022,12,6),
        lbs_per_day = 2/7,
        birthdate = date(1992,12,5),
        sex = 'male',
        activity_level = 1.2,
        goal_weight = 150,
        user_logs = [food_log],
    )