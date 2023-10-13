from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.crud import crud
from app import models
from app import schemas
from app.api.calcs.calorie_calcs import PersonsDay
from datetime import date, timedelta
import json
import pytest

profile = {"id":1, "start_date": '2023-04-09', "start_weight": 803.3, "goal_weight": 241.0, "sex": 'Male', "birthdate": '1994-10-26', "height": 10, "lbs_per_week": 1.38, "activity_level": 1.8, "user_id": 1, "log": []}

async def test_never_faultered_prediction(client:TestClient, db:Session):
    params = {'height':profile['height'], 'start_weight':profile['start_weight'], 'start_date':profile['start_date'], 'lbs_per_week':profile['lbs_per_week'], 'birthdate':profile['birthdate'], 'sex':profile['sex'], 'activity_level':profile['activity_level'], 'goal_weight':profile['goal_weight'], 'log':profile['log']}

    response= await client.get(f"/api/v1/predictions/never_faulter", params=params)

    assert response.status_code == 200
    assert response.json() is not None

async def test_current_average_weekly_loss(client:TestClient, db:Session):
    params = {'height':profile['height'], 'start_weight':profile['start_weight'], 'start_date':profile['start_date'], 'lbs_per_week':profile['lbs_per_week'], 'birthdate':profile['birthdate'], 'sex':profile['sex'], 'activity_level':profile['activity_level'], 'goal_weight':profile['goal_weight'], 'log':profile['log']}

    response= await client.get(f"/api/v1/predictions/update_lbs_to_lose?current_date=2022-12-06", params=params)
    assert response.status_code == 200
    assert response.json() is not None


async def test_prediction_never_faulter(daily_output:PersonsDay):
    with open('app/tests/test_data/prediction.json') as prediction_file:
        prediction_output = json.load(prediction_file)
    # daily = await daily_output
    assert daily_output.prediction() == prediction_output

def test_prediction_update_weekly_lbs_loss(daily_output:PersonsDay):
    current_date = date(2022,12,7)
    total_days = (current_date - daily_output.start_date).days
    
    if total_days:
        daily_output.lbs_per_day = daily_output.total_lbs_lost(current_date=current_date) / total_days

    pred = daily_output.prediction()  
    
    with open('app/tests/test_data/prediction_update_weekly_lbs_lost.json') as prediction_file:
        prediction_output = json.load(prediction_file)


    assert pred == prediction_output


async def test_goal_weight_higher_than_start(client:TestClient, db:Session):
    params = {'height':profile['height'], 'start_weight':301.0, 'start_date':profile['start_date'], 'lbs_per_week':profile['lbs_per_week'], 'birthdate':profile['birthdate'], 'sex':profile['sex'], 'activity_level':profile['activity_level'], 'goal_weight':500.0, 'log':profile['log']}

    response= await client.get(f"/api/v1/predictions/never_faulter", params=params)

    assert response.status_code == 404
    assert response.json() == {"detail":"Goal Weight greater than Start Weight"}

async def test_goal_weight_too_low(client:TestClient, db:Session):
    params = {'height':profile['height'], 'start_weight':profile['start_weight'], 'goal_weight':10.0, 'start_date':profile['start_date'], 'lbs_per_week':profile['lbs_per_week'], 'birthdate':profile['birthdate'], 'sex':profile['sex'], 'activity_level':profile['activity_level'], 'log':profile['log']}

    response= await client.get(f"/api/v1/predictions/never_faulter", params=params)

    assert response.status_code == 404
    assert response.json() == {"detail":"Goal weight resting calories are less than lowest allowed calories"}