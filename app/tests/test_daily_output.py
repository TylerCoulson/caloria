from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from datetime import date, timedelta, datetime
from fastapi.encoders import jsonable_encoder
from app import crud
from . import utils
from app import schemas
from app import models
from app.api.calcs import calorie_calcs


async def get_weight(profile_id, current_date, db):
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()

async def test_daily_overview_get(client:TestClient, db:Session, food_log:models.Food_Log):    
    start_date = datetime.strptime(food_log['profile']['start_date'],'%Y-%m-%d')
    end_date = datetime.strptime(food_log['date'],'%Y-%m-%d')

    days = (end_date - start_date).days 

    data = {
        "current_date": food_log['date'],
        "actual_weight": 308.8
    }

    response= await client.get(f"/api/v1/daily/{data['current_date']}")

    assert response.status_code == 200
    content = response.json()

    output = {
        "day": days,
        "actual_weight": 0,
        "week": days//7 + 1,
        "date": end_date,
        "est_weight": 311.7,
        "resting_rate": 2860,
        "eaten_calories": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": food_log['profile_id'],
        "bmi": 44.71
    }

    assert content.keys() == output.keys()

async def test_daily_overview_post(client:TestClient, db:Session, profile: models.Profile, food_log:models.Food_Log):
    start_date = datetime.strptime(food_log['profile']['start_date'],'%Y-%m-%d')

    data = {
        "profile_id": profile['id'],
        "date": (start_date).strftime('%Y-%m-%d'),
        "actual_weight": 308.8
    }
    response = await client.post(f"/api/v1/daily", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['actual_weight'] == 308.8

    statement = select(models.DailyLog.profile_id)
    weight_data = await db.execute(statement)
    weight_id = weight_data.unique().first()
    # await crud.delete(_id=weight_id, db=db, db_obj=weight_data)

async def test_daily_overview_update(client:TestClient, db:Session, food_log_2:models.Food_Log):    
    daily = {
        "profile_id": food_log_2['profile']['id'],
        "date": food_log_2['date'],
        "actual_weight": 308.8
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data.actual_weight == 256.7
    response= await client.put(f"/api/v1/daily/{data.date}", json=jsonable_encoder(data))
    assert response.status_code == 200
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 256.7,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "resting_rate": 2860,
        "eaten_calories": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": food_log_2['profile_id'],
        "bmi":44.71
    }

    assert content.keys() == output.keys() 

async def test_daily_overview_delete(client:TestClient, db:Session, profile, food_log:models.Food_Log):    
    end_date = "2023-12-07"

    daily = {
        "profile_id": food_log['profile']['id'],
        "date": end_date,
        "actual_weight": 308.8
    }
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    response= await client.delete(f"/api/v1/daily/{data.date}")
    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=data.id, db=db, model=models.DailyLog)  is None