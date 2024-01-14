from datetime import timedelta, datetime
from app import crud
from app import schemas
from app import models

async def test_daily_overview_post_acutal_weight(client, module_profile):

    data = {
        "profile_id": 1,
        "date": module_profile['start_date'],
        "actual_weight": 308.8,
    }
    response = await client.post(f"/api/v1/daily?actual_weight=True", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['actual_weight'] == 308.8

async def test_daily_overview_post_activity_level(client, module_profile):

    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    data = {
        "profile_id": 1,
        "date": (start_date + timedelta(days=1)).date().strftime('%Y-%m-%d'),
        "activity_level": 1.8,
    }
    response = await client.post(f"/api/v1/daily?activity_level=True", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['activity_level'] == 1.8

async def test_daily_overview_post_wrong_id(client, module_profile):

    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    data = {
        "profile_id": 4,
        "date": (start_date + timedelta(days=2)).date().strftime('%Y-%m-%d'),
        "activity_level": 1.8,
    }

    response = await client.post(f"/api/v1/daily?activity_level=True", json=data)
    content = response.json()    
    assert response.status_code == 201

    assert content['activity_level'] == 1.8
    assert content['profile_id'] == 1

async def test_daily_overview_post_activity_level_with_established_actual_weight(client, db, module_profile):    
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=3)).date().strftime('%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 255
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    data = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 2.7
    }

    response= await client.post(f"/api/v1/daily?activity_level=True", json=data)
    assert response.status_code == 201
    content = response.json()

    assert content['actual_weight'] == 255
    assert content['activity_level'] == 2.7

async def test_daily_overview_post_actual_weight_with_established_activity_level(client, db, module_profile):
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=4)).date().strftime('%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 1.5
        
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    data = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 324
    }

    response = await client.post(f"/api/v1/daily?actual_weight=True", json=data)
    assert response.status_code == 201
    content = response.json()

    assert content['actual_weight'] == 324
    assert content['activity_level'] == 1.5

async def test_daily_overview_post_both_actual_weight_and_activity_level(client, module_profile):
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=5)).date().strftime('%Y-%m-%d')
    data = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 158,
        "activity_level":1.3
    }

    response = await client.post(f"/api/v1/daily?actual_weight=True&activity_level=True", json=data)
    assert response.status_code == 201
    content = response.json()

    assert content['actual_weight'] == 158
    assert content['activity_level'] == 1.3