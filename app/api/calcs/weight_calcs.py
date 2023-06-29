from app import models, schemas
from sqlalchemy import select, func, extract, cast, Integer, literal, union_all, or_, column, Date, Interval, Text
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, datetime, timedelta


async def get_db_data(profile:models.Profile, db: Session):

    start_date = datetime.strptime(profile.start_date, '%Y-%m-%d').date()
    end_date = date.today()
    dates = [start_date + timedelta(days=d) for d in range((end_date - start_date).days + 1)]
 
    subqueries = [select(literal(date).label("dates")) for date in dates]
        
    subquery = union_all(*subqueries).alias("dates")
    
    statement = select(
        subquery.c.dates.label("date"),
        func.sum(models.ServingSize.calories * models.Food_Log.serving_amount).label("calories_eaten"),
        column(str((profile.height*2.54) * 6.25)).label("height_calc"),
        (cast((extract('epoch', subquery.c.dates) - extract('epoch', profile.birthdate))/60/60/24/365.25, Integer) * 5).label("age"),
        column(str(-161 if profile.sex == 'female' else 5)).label("sex"),
        column(str(profile.activity_level)).label("activity_level"),
        (cast((extract('epoch', subquery.c.dates) - extract('epoch', profile.start_date))/60/60/24, Integer)+1).label("days"),
        column(str(profile.lbs_per_week * 500)).label("goal_calories_per_week"),
        column(str(1200 if profile.sex == 'female' else 1500)).label("lowest_calories"),
        column(str(profile.height * profile.height)).label("heigh_squared"), # (used for bmi calc)
        models.DailyLog.actual_weight.label("user_inputed_weight"),
    ).select_from(subquery.outerjoin(models.Food_Log, models.Food_Log.date == subquery.c.dates)                                           
    ).where(or_(models.Food_Log.profile_id == profile.id, models.Food_Log.profile_id == None)
    ).join(models.ServingSize, isouter=True
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, isouter=True
    ).group_by(subquery.c.dates
    ).order_by(subquery.c.dates)
    
    result = await db.execute(statement)
    return result.unique().all()

async def transform_daily(profile:models.Profile, data):
    logs = []

    total_rmr = 0
    est_weight = profile.start_weight
    total_calorie_goal = 0
    previous_total_eaten = 0
    
    for i in data:
        weight_calc = 10 * (est_weight/2.2)
        total_calories_eaten = float(i[1]) if i[1] else 0
        height_calc = float(i[2])
        age_calc = float(i[3])
        sex_calc = float(i[4])
        act_level = float(i[5])
        resting_rate = ( (weight_calc+height_calc-age_calc) + sex_calc) * act_level
        day = i[6]


        total_rmr += resting_rate

        calorie_goal = max(resting_rate - float(i[7]), float(i[8]))
        total_calorie_goal += calorie_goal

        log = {
            "date": i[0],
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
            'bmi':round((est_weight/float(i[9]))*703,2),
            'actual_weight': i[10] or 0
        }
        

        previous_total_eaten = total_calories_eaten
        logs.append(log)
        est_weight = profile.start_weight-((total_rmr - total_calories_eaten)/3500)
    # logs.reverse()
    return logs

async def daily_log(profile:models.Profile, db: Session):

    if profile is None:
        raise ValueError("profile cannot be None")
 
    data = await get_db_data(profile, db)
    logs = await transform_daily(profile, data)
    
    return logs