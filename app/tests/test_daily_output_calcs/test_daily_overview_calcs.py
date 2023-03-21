from fastapi.encoders import jsonable_encoder
from datetime import date, timedelta, datetime
import json
from app import models
from app.api.calcs.calorie_calcs import PersonsDay

def test_prediction_never_faulter(daily_output:PersonsDay):
    with open('app/tests/test_data/prediction.json') as prediction_file:
        prediction_output = json.load(prediction_file)
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