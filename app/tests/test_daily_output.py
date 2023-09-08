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

async def test_daily_overview_get_before_start_date(client:TestClient, db:Session):    
    food_log = { "id":12, "date":'2023-04-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')

    response= await client.get(f"/api/v1/daily/{(start_date - timedelta(days=1)).date()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Date is before profile start date"}


async def test_daily_overview_get_on_start_date(client:TestClient, db:Session):    
    food_log = { "id":12, "date":'2023-04-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')
    end_date = datetime.strptime(food_log['date'],'%Y-%m-%d')

    days = (end_date - start_date).days 

    response= await client.get(f"/api/v1/daily/{start_date.date()}")

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

async def test_get_daily_after_start_date(client:TestClient, db:Session):
    food_log = { "id":12, "date":'2023-04-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')
    end_date = (start_date + timedelta(days=1)).date()
    days = 1 
    
    response= await client.get(f"/api/v1/daily/{end_date}")
    content = response.json()
    assert response.status_code == 200
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


async def test_daily_overview_post(client:TestClient, db:Session):
    food_log = { "id":12, "date":'2023-04-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')

    data = {
        "profile_id": 1,
        "date": (start_date).strftime('%Y-%m-%d'),
        "actual_weight": 308.8
    }
    response = await client.post(f"/api/v1/daily", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['actual_weight'] == 308.8

async def test_daily_overview_update(client:TestClient, db:Session):    
    food_log = { "id":12, "date":'2023-04-10', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": food_log['date'],
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
        "profile_id": 1,
        "bmi":44.71
    }

    assert content.keys() == output.keys() 

async def test_daily_overview_delete_by_date(client:TestClient, db:Session):    
    end_date = "2023-12-07"

    daily = {
        "profile_id": 1,
        "date": end_date,
        "actual_weight": 308.8
    }
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    response= await client.delete(f"/api/v1/daily/{data.date}")
    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=data.id, db=db, model=models.DailyLog)  is None

async def test_daily_overview_delete_by_id(client:TestClient, db:Session):    
    end_date = "2023-12-07"

    daily = {
        "profile_id": 1,
        "date": end_date,
        "actual_weight": 308.8
    }
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    response= await client.delete(f"/api/v1/daily/{data.id}")
    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=data.id, db=db, model=models.DailyLog)  is None

async def test_get_all_daily_valid_profile_n25_page1(client:TestClient, db:Session):
    response = await client.get("/api/v1/daily", params={"n": 25, "page": 1})
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_all_daily_valid_profile_n10_page2(client:TestClient, db:Session):
    response = await client.get("/api/v1/daily", params={"n": 10, "page": 2})
    assert response.status_code == 200
    assert len(response.json()) == 10

async def test_get_all_daily_valid_profile_n50_page3(client:TestClient, db:Session):
    response = await client.get("/api/v1/daily", params={"n": 50, "page": 3})
    assert response.status_code == 200
    assert len(response.json()) == 50
