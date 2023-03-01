from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from datetime import date, timedelta, datetime
from fastapi.encoders import jsonable_encoder
from app import crud
from . import utils
from app import schemas
from app import models
from app.api.calcs import calorie_calcs

def test_daily_overview_get(client:TestClient, db:Session, profile:models.Profile, food_log:models.Food_Log):    
    start_date = profile.start_date
    end_date = food_log.date
    days = (end_date - start_date).days 

    data = {
        "profile_id": profile.id,
        "current_date": end_date,
        "actual_weight": 308.8
    }

    response= client.get(f"/api/v1/daily/{data['profile_id']}/{data['current_date']}")
    
    assert response.status_code == 200
    content = response.json()

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
        "profile_id": food_log.profile_id,
        "bmi": 44.71
    }

    assert content.keys() == output.keys()

def test_daily_overview_post(client:TestClient, db:Session, profile: models.Profile):

    data = {
        "profile_id": profile.id,
        "date": (profile.start_date + timedelta(32)).isoformat(),
        "actual_weight": 308.8
    }
    response= client.post(f"/api/v1/daily", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['actual_weight'] == 308.8

def test_daily_overview_update(client:TestClient, db:Session, profile:models.Profile, food_log:models.Food_Log):    
    start_date = profile.start_date
    end_date = food_log.date
    days = (end_date - start_date).days 

    daily = {
        "profile_id": profile.id,
        "date": end_date.isoformat(),
        "actual_weight": 308.8
    }
    data = crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)

    data.actual_weight == 256.7

    response= client.put(f"/api/v1/daily/{data.profile_id}/{data.date}", json=jsonable_encoder(data))
    assert response.status_code == 200
    content = response.json()

    output = {
        "day": days,
        "actual_weight": 256.7,
        "week": days//7 + 1,
        "date": end_date.isoformat(),
        "est_weight": 311.7,
        "resting_rate": 2860,
        "eaten_calories": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": food_log.profile_id,
        "bmi":44.71
    }

    assert content.keys() == output.keys() 

def test_daily_overview_delete(client:TestClient, db:Session, profile:models.Profile, food_log:models.Food_Log):    
    end_date = food_log.date


    daily = {
        "profile_id": profile.id,
        "date": end_date.isoformat(),
        "actual_weight": 308.8
    }
    data = crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    response= client.delete(f"/api/v1/daily/{data.profile_id}/{data.date}")
    assert response.status_code == 200

    assert response.json() is None

    assert crud.read(_id=data.id, db=db, model=models.DailyLog) is None