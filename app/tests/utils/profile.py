import pytest
from app import models, schemas, crud

@pytest.fixture()
async def create_profile() -> models.Profile:
    return {"id":1001, "start_date": '2023-04-09', "start_weight": 803.3, "goal_weight": 241.0, "sex": 'Male', "birthdate": '1994-10-26', "height": 10, "lbs_per_week": 1.38, "activity_level": 1.8, "user_id": 1001}

@pytest.fixture()
async def get_profile() -> models.Profile:
    return {"id":1, "start_date": '2022-12-06', "start_weight": 322.4, "goal_weight": 150.0, "sex": 'Male', "birthdate": '1992-12-05', "height": 70, "lbs_per_week": 2.0, "activity_level": 2.0, "user_id": 1}


@pytest.fixture()
async def update_profile() -> models.Profile:
    return {"id":1, "start_date": '2023-12-06', "start_weight": 321.4, "goal_weight": 151.0, "sex": 'Female', "birthdate": '1992-12-05', "height": 70, "lbs_per_week": 1.0, "activity_level": 1.2, "user_id": 1}