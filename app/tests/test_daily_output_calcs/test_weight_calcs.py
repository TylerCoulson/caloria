from app.api.calcs.weight_calcs import transform_daily
from datetime import date
import pytest
from app import schemas

data = {
    '2023-09-06': {'date': date(2023, 9, 6), 'calories_eaten_today': 1790.0, 'user_inputed_weight': None},
    '2023-09-07': {'date': date(2023, 9, 7), 'calories_eaten_today': 1594.0, 'user_inputed_weight': None}
}
profile = {"id":1, "start_date": '2023-09-06', "start_weight": 322.4, "goal_weight": 150.0, "sex": 'Male', "birthdate": '1992-12-05', "height": 70, "lbs_per_week": 2.0, "activity_level": 1.2, "user_id": 1}
@pytest.mark.asyncio
async def test_transform_daily():
    t = await transform_daily(profile=schemas.Profile(**profile), data=data, end_date=date(2023, 9, 7))
    
    assert t == [
        {'date': date(2023, 9, 7), 'profile_id': 1, 'day': 2, 'week': 1, 'est_weight': 322.1, 'resting_rate': 2916.0, 'eaten_calories': 1594.0, 'calorie_goal': 1916.0, 'total_lbs_lost': 0.7, 'calorie_surplus': 450.0, 'calories_left': 322.0, 'bmi': 46.21, 'actual_weight': 0},
        {'date': date(2023, 9, 6), 'profile_id': 1, 'day': 1, 'week': 1, 'est_weight': 322.4, 'resting_rate': 2918.0, 'eaten_calories': 1790.0, 'calorie_goal': 1918.0, 'total_lbs_lost': 0.32, 'calorie_surplus': 128.0, 'calories_left': 128.0, 'bmi': 46.25, 'actual_weight': 0}
    ]