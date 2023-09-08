from app import models, schemas
from sqlalchemy import select, func, extract, cast, Integer, literal, union_all, or_, column, Date, Interval, Text
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, datetime, timedelta


async def get_db_data(profile:models.Profile, db: Session):


    # start_date = profile.start_date if type(profile.start_date) is date else datetime.strptime(profile.start_date, '%Y-%m-%d').date()
    # end_date = date.today()
    # dates = [start_date + timedelta(days=d) for d in range((end_date - start_date).days + 1)]
 
    # subqueries = [select(literal(date).label("dates")) for date in dates]
        
    # subquery = union_all(*subqueries).alias("dates")
    
    statement = select(
        models.Food_Log.date,
        func.sum(models.ServingSize.calories * models.Food_Log.serving_amount).label("calories_eaten_today"),
        func.max(models.DailyLog.actual_weight).label("user_inputed_weight")                            
    ).where(models.Food_Log.profile_id == profile.id
    ).join(models.ServingSize, isouter=True
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, isouter=True
    ).group_by(models.Food_Log.date
    ).order_by(models.Food_Log.date)

    result = await db.execute(statement)

    # covert from Row object to dictionary
    all_rows = result.unique().all()
    print({date.strftime(v.date, '%Y-%m-%d'): v._asdict() for v in all_rows})
    return {date.strftime(v.date, '%Y-%m-%d'): v._asdict() for v in all_rows}

async def transform_daily(profile:models.Profile, data:dict, end_date:date=date.today()):
    # set dates
    birthdate = profile.birthdate if type(profile.birthdate) is date else datetime.strptime(profile.birthdate, '%Y-%m-%d').date()
    start_date = profile.start_date if type(profile.start_date) is date else datetime.strptime(profile.start_date, '%Y-%m-%d').date()
    
    # create dictionary with all dates
    dates_dict = {}
    for d in range((end_date - start_date).days + 1):
        key = date.strftime(start_date + timedelta(days=d), "%Y-%m-%d")
        dates_dict[key] = {'date': start_date + timedelta(days=d), 'calories_eaten_today': 0.0, 'user_inputed_weight': None}

    for k, v in data.items():
        dates_dict[k] = v
    

    # Health calcs that do not change
    sex_calc = -161 if profile.sex == 'female' else 5
    act_level = profile.activity_level
    height_calc = (profile.height*2.54) * 6.25

    # Calcs that are changed
    est_weight = profile.start_weight
    total_calorie_goal = 0
    previous_total_eaten = 0
    total_calories_eaten = 0
    total_rmr = 0

    # iteration to get all daily outpus
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