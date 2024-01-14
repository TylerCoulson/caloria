from app.api.calcs.weight_calcs import transform_daily
from datetime import date
import pytest
from app import schemas

data = {
    '2023-09-06': {'food_log_date': date(2023, 9, 6),'daily_log_date': None, 'calories_eaten_today': 1790.0, "fats_eaten_today": 110, "carbs_eaten_today": 120, "protein_eaten_today": 130, 'user_inputed_weight': None, "user_activity_level":None},
    '2023-09-07': {'food_log_date': None, 'daily_log_date': date(2023, 9, 7), 'calories_eaten_today': 3052.0, "fats_eaten_today": 210, "carbs_eaten_today": 220, "protein_eaten_today": 230, 'user_inputed_weight': None, "user_activity_level":1.8}
}
profile = {"id":1, "start_date": '2023-09-06', "start_weight": 322.4, "goal_weight": 150.0, "sex": 'Male', "birthdate": '1992-12-05', "height": 70, "lbs_per_week": 2.0, "activity_level": 1.2, "user_id": 1}
@pytest.mark.asyncio
async def test_transform_daily():
    t = await transform_daily(profile=schemas.Profile(**profile), data=data, end_date=date(2023, 9, 7))
    
    assert t == [
        {'date': date(2023, 9, 7), 'profile_id': 1, 'day': 2, 'week': 1, 'est_weight': 322.1, 'calories_burned': 4374.0, 'eaten_calories': 3052.0, "eaten_fats": 210, "eaten_carbs": 220, "eaten_protein": 230, 'calorie_goal': 3374.0, 'total_lbs_lost': 0.7,  'total_calorie_goal': 5292.0, 'total_calories_burned': 7292.0, 'total_calories_eaten': 4842.0,'calorie_surplus': 450.0, 'calories_left': 322.0, 'bmi': 46.21, 'actual_weight': 0, "activity_level": 1.8},
        {'date': date(2023, 9, 6), 'profile_id': 1, 'day': 1, 'week': 1, 'est_weight': 322.4, 'calories_burned': 2918.0, 'eaten_calories': 1790.0, "eaten_fats": 110, "eaten_carbs": 120, "eaten_protein": 130, 'calorie_goal': 1918.0, 'total_lbs_lost': 0.32, 'total_calorie_goal': 1918.0, 'total_calories_burned': 2918.0, 'total_calories_eaten': 1790.0, 'calorie_surplus': 128.0, 'calories_left': 128.0, 'bmi': 46.25, 'actual_weight': 0, "activity_level": 1.2}
    ]