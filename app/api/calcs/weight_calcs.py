from app import models, schemas
from sqlalchemy import select, func, cast, String, or_
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, datetime, timedelta


async def get_db_data(profile:models.Profile, db: Session):
    statement = select(
        models.Food_Log.date.label('food_log_date'),
        models.DailyLog.date.label('daily_log_date'),
        (func.coalesce(func.sum(models.ServingSize.calories * models.Food_Log.serving_amount), 0)).label("calories_eaten_today"),
        (func.coalesce(func.sum(models.ServingSize.calories * models.Food_Log.serving_amount), 0)).label("fats_eaten_today"),
        (func.coalesce(func.sum(models.ServingSize.calories * models.Food_Log.serving_amount), 0)).label("carbs_eaten_today"),
        (func.coalesce(func.sum(models.ServingSize.calories * models.Food_Log.serving_amount), 0)).label("protein_eaten_today"),
        func.max(models.DailyLog.actual_weight).label("user_inputed_weight")                            
    ).where(or_(models.Food_Log.profile_id == profile.id, models.DailyLog.profile_id == profile.id)
    ).join(models.ServingSize, isouter=True
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, full=True
    ).group_by(models.Food_Log.date, models.DailyLog.date
    ).order_by(models.Food_Log.date)

    result = await db.execute(statement)

    # covert from Row object to dictionary
    all_rows = result.unique().all()

    test = {date.strftime(v.food_log_date or v.daily_log_date, '%Y-%m-%d'): v._asdict() for v in all_rows}
    
    return test

async def transform_daily(profile:models.Profile, data:dict, end_date:date=date.today()):
    # set dates
    birthdate = profile.birthdate if type(profile.birthdate) is date else datetime.strptime(profile.birthdate, '%Y-%m-%d').date()
    start_date = profile.start_date if type(profile.start_date) is date else datetime.strptime(profile.start_date, '%Y-%m-%d').date()
    
    # create dictionary with all dates
    dates_dict = {}
    for d in range((end_date - start_date).days + 1):
        key = date.strftime(start_date + timedelta(days=d), "%Y-%m-%d")
        dates_dict[key] = {'date': start_date + timedelta(days=d), 'calories_eaten_today': 0.0, 'fats_eaten_today':0.0, 'carbs_eaten_today':0.0, 'protein_eaten_today':0.0, 'user_inputed_weight': None}

    for k, v in data.items():
        v['date'] = v['food_log_date'] or v['daily_log_date']
        dates_dict[k] = v
    

    # Health calcs that do not change
    sex_calc = -161 if profile.sex == 'female' else 5
    act_level = profile.activity_level
    height_calc = (profile.height*2.54) * 6.25

    # Calcs that are changed
    est_weight = profile.start_weight
    total_calorie_goal = 0
    total_calories_eaten = 0
    total_rmr = 0

    # iteration to get all daily outpus.date
    logs = []
    for k, v in dates_dict.items():
        weight_calc = 10 * (est_weight/2.2)
        calories_eaten_today = round(v["calories_eaten_today"],0)
        age_calc = int((v["date"] - birthdate).days/365.25) * 5
        resting_rate = round(((weight_calc+height_calc-age_calc) + sex_calc) * act_level,0)
        day = (v["date"] - start_date).days +1

        calorie_goal = max(resting_rate - profile.lbs_per_week * 500, 1200 if profile.sex == 'female' else 1500)

        total_rmr += resting_rate
        total_calories_eaten += calories_eaten_today
        total_calorie_goal += calorie_goal

        log = {
            "date": v["date"],
            "profile_id":profile.id,
            'day':day,
            'week':(day//7)+1,
            'est_weight':round(est_weight,1),
            'resting_rate':resting_rate,
            'eaten_calories':round(calories_eaten_today,0),
            'eaten_fats':round(v["fats_eaten_today"],0),
            'eaten_carbs':round(v["carbs_eaten_today"],0),
            'eaten_protein':round(v["protein_eaten_today"],0),
            'calorie_goal': round(calorie_goal,0),
            'total_lbs_lost':round((total_rmr - total_calories_eaten)/3500,2),
            'calorie_surplus': round(total_calorie_goal - total_calories_eaten,0),
            'calories_left':round(calorie_goal - calories_eaten_today,0),
            'bmi':round((est_weight/float(profile.height**2))*703,2),
            'actual_weight': v["user_inputed_weight"] or 0
        }
        

        logs.append(log)
        est_weight -= (resting_rate-calories_eaten_today)/3500
    
    logs.reverse()
    return logs


async def daily_log(profile:models.Profile, db: Session):

    if profile is None:
        raise ValueError("profile cannot be None")
 
    data = await get_db_data(profile, db)
    logs = await transform_daily(profile, data)
    
    return logs