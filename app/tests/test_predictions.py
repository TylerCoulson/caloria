from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.crud import crud
from app import models
from app import schemas
from datetime import date, timedelta

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


