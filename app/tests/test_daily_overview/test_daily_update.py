from datetime import timedelta, datetime
from app import crud
from app import schemas
from app import models

async def test_daily_overview_update_actual_weight(client, module_profile, db):
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=10)).date().strftime('%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 308.8
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    daily['actual_weight'] = 256.7

    response = await client.put(f"/api/v1/daily/{daily['date']}?actual_weight=True", json=daily)
    assert response.status_code == 200
    content = response.json()


    assert content['actual_weight'] == 256.7
    assert content['activity_level'] == module_profile['activity_level']
 
async def test_daily_overview_update_activity_level(client, module_profile, db):
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=11)).date().strftime('%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 1.2
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    daily['activity_level'] = 1.8
    response = await client.put(f"/api/v1/daily/{daily['date']}?activity_level=True", json=daily)
    assert response.status_code == 200
    content = response.json()


    assert content['activity_level'] == 1.8
    assert content['actual_weight'] == 0

async def test_daily_overview_update_actual_weight_with_established_activity_level(client, module_profile, db):    

    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=12)).date().strftime('%Y-%m-%d')
    daily = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 1.5,
        "actual_weight": 315
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    data = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 324
    }

    response = await client.put(f"/api/v1/daily/{daily['date']}?actual_weight=True", json=data)
    assert response.status_code == 200
    content = response.json()

    assert content['actual_weight'] == 324
    assert content['activity_level'] == 1.5

async def test_daily_overview_update_activity_level_with_established_actual_weight(client, module_profile, db):    
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=13)).date().strftime('%Y-%m-%d')
    
    daily = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 255,
        "activity_level": 1.2
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    data = {
        "profile_id": 1,
        "date": test_date,
        "activity_level": 2.7
    }

    response = await client.put(f"/api/v1/daily/{test_date}?activity_level=True", json=data)
    assert response.status_code == 200
    content = response.json()

    assert content['actual_weight'] == 255
    assert content['activity_level'] == 2.7

async def test_daily_overview_update_activity_and_actual_weight(client, module_profile, db):
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')
    test_date = (start_date + timedelta(days=14)).date().strftime('%Y-%m-%d')
    
    daily = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 255,
        "activity_level": 1.2
    }
    
    data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=schemas.Profile(**module_profile))


    data = {
        "profile_id": 1,
        "date": test_date,
        "actual_weight": 155,
        "activity_level": 2.7
    }

    response = await client.put(f"/api/v1/daily/{test_date}?activity_level=True&actual_weight=True", json=data)
    assert response.status_code == 200
    content = response.json()

    assert content['actual_weight'] == 155
    assert content['activity_level'] == 2.7