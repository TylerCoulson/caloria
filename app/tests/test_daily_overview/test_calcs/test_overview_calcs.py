from datetime import timedelta
from app.api.calcs.calorie_calcs import PersonsDay


def test_bmi(daily_output:PersonsDay):
    current_date = daily_output.start_date
    assert daily_output.bmi(current_date=current_date) == 46.25


def test_total_calories_eaten(daily_output:PersonsDay):
    current_date = daily_output.start_date + timedelta(1)
    assert daily_output.total_calories_eaten(current_date=current_date) == 500

def test_estimated_weight(daily_output:PersonsDay):
    current_date = daily_output.start_date + timedelta(1)
    est_weight = daily_output.estimated_weight(current_date=current_date) 
    assert est_weight == 321.7

def test_calories_eaten_on_date(daily_output:PersonsDay):
    current_date = daily_output.start_date + timedelta(1)
    assert daily_output.calories_eaten_on_date(current_date=current_date) == 500