import random
import string
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from datetime import date, timedelta

def random_lower_string(k=32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_date(start:date=date(1923,1,1), end:date=date(2010,12,31)) -> date:
    days_difference = end - start
    random_date = start + timedelta(days=days_difference.days) * random.random() 
    
    return random_date

def create_random_user_dict() -> dict:
    start_date = date.today()
    email = f'{random_lower_string()}@{random_lower_string(6)}.com'
    start_weight = random.randint(200,700) + round(random.random(),2)
    end_weight = random.randint(100,180) + round(random.random(),2)
    sex = random.choice(['male', "female"])
    birthdate = random_date()
    height = random.randint(48,84)
    lbs_to_lost = round(random.random() * 2)
    activity_level = random.choice([1.2,1.375,1.55,1.725,1.9])

    user_dict = schemas.UserCreate(
        start_date = start_date,
        email = email,
        start_weight = start_weight,
        end_weight = end_weight,
        sex = sex,
        birthdate = birthdate,
        height = height,
        lbs_to_lost = lbs_to_lost,
        activity_level = activity_level,
    )

    return jsonable_encoder(user_dict)

def create_random_user(db, user_dict) -> models.User:
    data = schemas.UserCreate(**user_dict)
    user = crud.create(obj_in=data, db=db, model=models.User)
    return jsonable_encoder(user)

def create_random_food(db) -> models.Food:
    brand = random_lower_string()
    name = random_lower_string()
    food_dict = schemas.FoodCreate(brand= brand, name= name)

    food = crud.create(obj_in=food_dict, db=db, model=models.Food)

    return jsonable_encoder(food)

def create_random_serving_size(food_id, db) -> models.ServingSize:
    data = schemas.ServingSizeCreate(
        food_id = food_id,
        description = random_lower_string(),
        calories = random.randint(1,1000),
        fats = random.randint(1,1000),
        carbs = random.randint(1,1000),
        protein = random.randint(1,1000),
    )


    serving = crud.create(obj_in=data, db=db, model=models.ServingSize)
    return jsonable_encoder(serving)


def create_food_log(user_id:int, food_id:int, serving_size_id:int, date:date, db) -> models.Food_Log:
    data = {
        "date": date.isoformat(), 
        "food_id": food_id,
        "serving_size_id": serving_size_id,
        "serving_amount": random.randint(1,10),
        "user_id": user_id
    }

    data = schemas.FoodLogCreate(**data)
    log = crud.create(obj_in=data, db=db, model=models.Food_Log)
    return jsonable_encoder(log)