from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from datetime import date, timedelta, datetime
from . import utils
from app import schemas
from app import models
from app.api.calcs import calorie_calcs

def test_daily_data(client:TestClient, db:Session, user:models.User, food_log:models.Food_Log):    
    start_date = user.start_date
    end_date = food_log.date
    days = calorie_calcs.days_between(start_date, end_date)

    data = {
        "user_id": user.id,
        "date": end_date,
        "actual_weight": 308.8
    }

    response= client.get(f"/api/v1/daily/{data['user_id']}/{data['date']}")
    assert response.status_code == 200
    content = response.json()

    # assert 1 == 2
    output = {
        "day": days,
        "actual_weight": 0,
        "week": days//7 + 1,
        "date": end_date.isoformat(),
        "est_weight": 311.7,
        "resting_rate": 2860,
        "eaten_calories": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "user_id": food_log.user_id
    }

    assert content.keys() == output.keys()

def test_add_actual_weight(client:TestClient, db:Session, user: models.User):

    data = {
        "user_id": user.id,
        "date": (user.start_date + timedelta(32)).isoformat(),
        "actual_weight": 308.8
    }
    response= client.post(f"/api/v1/daily", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['actual_weight'] == 308.8