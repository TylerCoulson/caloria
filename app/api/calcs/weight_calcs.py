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
        func.sum(models.ServingSize.calories * models.Food_Log.serving_amount).label("calories_eaten"),
        func.max(models.DailyLog.actual_weight).label("user_inputed_weight")                            
    ).where(models.Food_Log.profile_id == profile.id
    ).join(models.ServingSize, isouter=True
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, isouter=True
    ).group_by(models.Food_Log.date
    ).order_by(models.Food_Log.date)

    result = await db.execute(statement)
    return result.unique().all()

async def transform_daily(profile:models.Profile, data):
    birthdate = profile.birthdate if type(profile.birthdate) is date else datetime.strptime(profile.birthdate, '%Y-%m-%d').date()
    start_date = profile.start_date if type(profile.start_date) is date else datetime.strptime(profile.start_date, '%Y-%m-%d').date()
    logs = []

    total_rmr = 0
    est_weight = profile.start_weight
    total_calorie_goal = 0
    previous_total_eaten = 0
    
    for i in data:
        weight_calc = 10 * (est_weight/2.2)
        total_calories_eaten = float(i.calories_eaten) if i.calories_eaten else 0
        height_calc = (profile.height*2.54) * 6.25
        age_calc = int((i.date - birthdate).days/365.25) * 5
        sex_calc = -161 if profile.sex == 'female' else 5
        act_level = profile.activity_level
        resting_rate = ( (weight_calc+height_calc-age_calc) + sex_calc) * act_level
        day = (i.date - start_date).days +1


        total_rmr += resting_rate

        calorie_goal = max(resting_rate - profile.lbs_per_week * 500, 1200 if profile.sex == 'female' else 1500)
        total_calorie_goal += calorie_goal

        log = {
            "date": i.date,
            "profile_id":profile.id,
            'day':day,
            'week':(day//7)+1,
            'est_weight':round(est_weight,1),
            'resting_rate':round(resting_rate,0),
            'eaten_calories':round(total_calories_eaten - previous_total_eaten,0),
            'calorie_goal': round(calorie_goal,0),
            'total_lbs_lost':round((total_rmr - total_calories_eaten)/3500,2),
            'calorie_surplus': round(total_calorie_goal - total_calories_eaten,0),
            'calories_left':round(calorie_goal - (total_calories_eaten-previous_total_eaten),0),
            'bmi':round((est_weight/float(profile.height**2))*703,2),
            'actual_weight': i.user_inputed_weight or 0
        }
        

        previous_total_eaten = total_calories_eaten
        logs.append(log)
        est_weight = profile.start_weight-((total_rmr - total_calories_eaten)/3500)
    return logs

async def daily_log(profile:models.Profile, db: Session):

    if profile is None:
        raise ValueError("profile cannot be None")
 
    data = await get_db_data(profile, db)
    logs = await transform_daily(profile, data)
    
    return logs