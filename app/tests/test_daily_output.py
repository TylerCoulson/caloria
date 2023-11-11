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
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": food_log['profile_id'],
        "bmi": 44.71,
        "activity_level": 1.2
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
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": food_log['profile_id'],
        "bmi": 44.71,
        "activity_level": 1.2
    }
    assert content.keys() == output.keys() 


async def test_daily_overview_post_acutal_weight(client:TestClient, db:Session):
    food_log = { "id":12, "date":'2023-04-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')

    data = {
        "profile_id": 1,
        "date": (start_date).strftime('%Y-%m-%d'),
        "actual_weight": 308.8,
    }
    response = await client.post(f"/api/v1/daily?actual_weight=True", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['actual_weight'] == 308.8

async def test_daily_overview_post_activity_level(client:TestClient, db:Session):
    food_log = { "id":12, "date":'2023-04-10', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')

    data = {
        "profile_id": 1,
        "date": (start_date).strftime('%Y-%m-%d'),
        "activity_level": 1.8,
    }
    response = await client.post(f"/api/v1/daily?activity_level=True", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['activity_level'] == 1.8

async def test_daily_overview_update_actual_weight(client:TestClient, db:Session):    
    food_log = { "id":12, "date":'2023-04-11', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": food_log['date'],
        "actual_weight": 308.8
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data.actual_weight = 256.7
    response= await client.put(f"/api/v1/daily/{data.date}", json=jsonable_encoder(data))
    assert response.status_code == 200
    content = response.json()
    print(data.actual_weight)
    output = {
        "day": 0,
        "actual_weight": 256.7,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.2
    }

    assert content.keys() == output.keys()
    assert content['actual_weight'] == 256.7

async def test_daily_overview_update_activity_level(client:TestClient, db:Session):    
    daily = {
        "profile_id": 1,
        "date": '2023-04-12',
        "activity_level": 1.2
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data.activity_level = 1.8
    response= await client.put(f"/api/v1/daily/{data.date}", json=jsonable_encoder(data))
    assert response.status_code == 200
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 256.7,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.8
    }

    assert content.keys() == output.keys()
    assert content['activity_level'] == 1.8

async def test_daily_overview_post_activity_level_with_established_actual_weight(client:TestClient, db:Session):    
    test_date = '2023-04-13'
    
    daily = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 255
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 2.7
    }

    response= await client.post(f"/api/v1/daily?activity_level=True", json=jsonable_encoder(data))
    assert response.status_code == 201
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 324,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.5
    }

    assert content.keys() == output.keys()
    assert content['actual_weight'] == 255
    assert content['activity_level'] == 2.7

async def test_daily_overview_post_actual_weight_with_established_activity_level(client:TestClient, db:Session):    
    food_log = { "id":12, "date":'2024-04-14', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": food_log['date'],
        "activity_level": 1.5
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data = {
        "profile_id": 1,
        "date": food_log['date'],
        "actual_weight": 324
    }

    response= await client.post(f"/api/v1/daily?actual_weight=True", json=jsonable_encoder(data))
    assert response.status_code == 201
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 324,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.5
    }

    assert content.keys() == output.keys()
    assert content['actual_weight'] == 324
    assert content['activity_level'] == 1.5

async def test_daily_overview_post_both_actual_weight_and_activity_level(client:TestClient, db:Session):
    data = {
        "profile_id": 1,
        "date": "2024-06-05",
        "actual_weight": 158,
        "activity_level":1.3
    }

    response= await client.post(f"/api/v1/daily?actual_weight=True&activity_level=True", json=jsonable_encoder(data))
    assert response.status_code == 201
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 158,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.2
    }

    assert content.keys() == output.keys()
    assert content['actual_weight'] == 158
    assert content['activity_level'] == 1.3

async def test_daily_overview_update_actual_weight_with_established_activity_level(client:TestClient, db:Session):    
    food_log = { "id":12, "date":'2024-04-17', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1}
    start_date = datetime.strptime(food_log['date'],'%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": food_log['date'],
        "activity_level": 1.5,
        "actual_weight": 315
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data = {
        "profile_id": 1,
        "date": food_log['date'],
        "actual_weight": 324
    }

    response= await client.put(f"/api/v1/daily/{daily['date']}?actual_weight=True", json=jsonable_encoder(data))
    assert response.status_code == 200
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 324,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.5
    }

    assert content.keys() == output.keys()
    assert content['actual_weight'] == 324
    assert content['activity_level'] == 1.5

async def test_daily_overview_update_activity_level_with_established_actual_weight(client:TestClient, db:Session):    
    test_date = '2023-04-18'
    
    daily = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 255,
        "activity_level": 1.2
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog)


    data = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 2.7
    }

    response= await client.put(f"/api/v1/daily/{test_date}?activity_level=True", json=jsonable_encoder(data))
    assert response.status_code == 200
    content = response.json()

    output = {
        "day": 0,
        "actual_weight": 324,
        "week": 0,
        "date": 0,
        "est_weight": 311.7,
        "calories_burned": 2860,
        "eaten_calories": 1900,
        "eaten_fats": 1900,
        "eaten_carbs": 1900,
        "eaten_protein": 1900,
        "calories_left": -40,
        "calorie_goal": 1860,
        "total_lbs_lost": 10.7,
        "calorie_surplus": -19540,
        "profile_id": 1,
        "bmi":44.71,
        "activity_level": 1.5
    }

    assert content.keys() == output.keys()
    assert content['actual_weight'] == 255
    assert content['activity_level'] == 2.7

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
