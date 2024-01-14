from fastapi.testclient import TestClient
from datetime import timedelta, datetime


async def test_daily_overview_get_before_start_date(client:TestClient, module_profile):    
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')

    response= await client.get(f"/api/v1/daily/{(start_date - timedelta(days=1)).date()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Date is before profile start date"}


async def test_daily_overview_get_on_start_date(client:TestClient, module_profile):    

    response= await client.get(f"/api/v1/daily/{module_profile['start_date']}")

    assert response.status_code == 200
    content = response.json()

    output = {
        "day": 1,
        "actual_weight": 0,
        "week": 1,
        "date": module_profile['start_date'],
        "est_weight": 322.4,
        "calories_burned": 4863,
        "eaten_calories": 533530,
        "eaten_fats": 79599,
        "eaten_carbs": 70116,
        "eaten_protein": 66690,
        "calories_left": -529667,
        "calorie_goal": 3863,
        "total_lbs_lost": -151.05,
        "calorie_surplus": -529667,
        "profile_id": module_profile['id'],
        "bmi": 46.25,
        "activity_level": 2.0
    }

    assert content == output

async def test_get_daily_after_start_date(client:TestClient, module_profile):
    start_date = datetime.strptime(module_profile['start_date'],'%Y-%m-%d')

    response= await client.get(f"/api/v1/daily/{(start_date + timedelta(days=1)).date()}") 
    
    content = response.json()
    assert response.status_code == 200
    output = {
        "day": 2,
        "actual_weight": 0,
        "week": 1,
        "date": (start_date + timedelta(days=1)).strftime('%Y-%m-%d'),
        "est_weight": 473.4,
        "calories_burned": 6237,
        "eaten_calories": 525836,
        "eaten_fats": 6172,
        "eaten_carbs": 5218,
        "eaten_protein": 42440,
        "calories_left": -520599,
        "calorie_goal": 5237,
        "total_lbs_lost": -299.5,
        "calorie_surplus": -1050266,
        "profile_id": module_profile['id'],
        "bmi": 67.93,
        "activity_level": 2.0
    }

    assert content == output 