from app.api.calcs.calorie_calcs import estimated_weight

def test_estimated_weight():
    total_calories_eaten = 129102.1
    start_weight = 322.4
    lbs_per_day = 2/7
    days = 58
    start_age = 30
    current_age = 30
    height = 70
    sex = "male"
    activity_level = 1.2

    est_weight = estimated_weight(total_calories_eaten=total_calories_eaten, start_weight=start_weight, lbs_per_day=lbs_per_day, days=days, start_age=start_age, current_age=current_age, height=height, sex=sex, activity_level=activity_level)

    assert est_weight == 311.7