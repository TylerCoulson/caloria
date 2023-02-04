from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from datetime import date, timedelta, datetime
from . import utils
from app import schemas
from app.api.calcs import calorie_calcs

def test_daily_data(client:TestClient, db:Session):
    user_dict = {
        "start_date":date(2022,12,6),
        "email":f'{utils.random_lower_string()}@{utils.random_lower_string(6)}.com',
        "start_weight":322.4,
        "end_weight":150,
        "sex":'male',
        "birthdate":date(1992,12,5),
        "height":70,
        "lbs_to_lost":2,
        "activity_level":1.2,
    }
    user = utils.create_user(db, user_dict)
    
    start_date = datetime.strptime(user['start_date'], "%Y-%m-%d").date()
    end_date = start_date + timedelta(days=58)
    days = calorie_calcs.days_between(start_date, end_date)


    large_food = utils.create_random_food(db)
    past_serving_size = schemas.ServingSizeCreate(
        food_id = large_food['id'],
        description = "large_serving",
        calories = 129102.1,
        fats = 1000,
        carbs = 1000,
        protein = 1000,
    )

    past_serving_size_db = utils.create_serving_size_db(past_serving_size, db)
    utils.create_food_log(user['id'], large_food['id'], past_serving_size_db['id'], date=start_date, db=db, serving_amount=1)

    current_serving_size = schemas.ServingSizeCreate(
        food_id = large_food['id'],
        description = "small_serving",
        calories = 1900,
        fats = 1,
        carbs = 1,
        protein = 1,
    )

    current_serving_size_db = utils.create_serving_size_db(current_serving_size, db)

    utils.create_food_log(user['id'], large_food['id'], current_serving_size_db['id'], date=end_date, db=db, serving_amount=1)


    data = {
        "user_id": user['id'],
        "date": end_date
    }
    response= client.get(f"/daily/{data['user_id']}/{data['date']}")
    assert response.status_code == 200
    content = response.json()
    
    # assert 1 == 2
    output = {
        "day": 58,
        "actual_weight": 0,
        "week": 9,
        "date":date(2023,2,2).isoformat(),
        "est_weight": 311.7,
        "resting_rate": 2860,
        "eaten_calories": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540
        
        ,
        "user_id": user['id']
    }

    assert content == output