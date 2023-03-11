from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.crud import crud
from app import models
from app import schemas
from datetime import date, timedelta



async def test_never_faultered_prediction(client:TestClient, db:Session, profile:models.Profile):

    response= await client.get(f"/api/v1/predictions/1/{profile['id']}")
    assert response.status_code == 200
    assert response.json() is not None

async def test_current_average_weekly_loss(client:TestClient, db:Session, profile:models.Profile):

    response= await client.get(f"/api/v1/predictions/2/{profile['id']}?current_date=2022-12-06")

    assert response.status_code == 200
    assert response.json() is not None


# async def test_mistep_then_back_on_track_prediction(client:TestClient, db:Session, profile:models.Profile):
#     output = {
#         "day": 2,
#         "week": 1,
#         "date": profile.start_date + timedelta(1),
#         "est_weight": 322.1,
#         "resting_rate": 2916,
#         "eaten_calories": 1916,
#         "calories_left": 0,
#         "calorie_goal": 1860,
#         "total_lbs_lost": 10.7,
#         "calorie_surplus": -19540,
#         "profile_id": profile.id,
#         "bmi": 44.71
#     }

#     response= client.get(f"/api/v1/predictions/2/{profile.id}")
    
#     assert response.status_code == 200
#     content = response.json()
#     assert content[0].keys() == output.keys()


