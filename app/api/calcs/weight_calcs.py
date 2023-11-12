from app import models, schemas
from sqlalchemy import select, func, cast, String, or_, and_
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, datetime, timedelta
from .day import Day, Log
from collections import OrderedDict

async def get_aggregate_food_logs_and_actual_weight(profile:models.Profile, db: Session):
    statement = select(
        models.Food_Log.date.label('food_log_date'),
        models.DailyLog.date.label('daily_log_date'),
        (func.coalesce(func.sum(models.ServingSize.calories * models.Food_Log.serving_amount), 0)).label("calories_eaten_today"),
        (func.coalesce(func.sum(models.ServingSize.fats * models.Food_Log.serving_amount), 0)).label("fats_eaten_today"),
        (func.coalesce(func.sum(models.ServingSize.carbs * models.Food_Log.serving_amount), 0)).label("carbs_eaten_today"),
        (func.coalesce(func.sum(models.ServingSize.protein * models.Food_Log.serving_amount), 0)).label("protein_eaten_today"),
        func.max(models.DailyLog.actual_weight).label("user_inputed_weight"),
        func.max(models.DailyLog.activity_level).label("user_activity_level")
    ).where(or_(models.Food_Log.profile_id == profile.id, models.DailyLog.profile_id == profile.id)
    ).where(
        and_(
            or_(models.DailyLog.date >= profile.start_date, models.DailyLog.date == None), 
            or_(models.Food_Log.date >= profile.start_date, models.Food_Log.date == None)
        )
    ).join(models.ServingSize, isouter=True
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, full=True
    ).group_by(models.Food_Log.date, models.DailyLog.date
    ).order_by(models.Food_Log.date)

    result = await db.execute(statement)

    # covert from Row object to dictionary
    all_rows = result.unique().all()

    test = {date.strftime(v.food_log_date or v.daily_log_date, '%Y-%m-%d'): v._asdict() for v in all_rows}
    
    return test



def create_dictionary_of_days(start_date:date, end_date:date):
    dates_dict = OrderedDict()
    for d in range((end_date - start_date).days + 1):
        key = date.strftime(start_date + timedelta(days=d), "%Y-%m-%d")
        dates_dict[key] = Day(date=start_date + timedelta(days=d))

    return dates_dict

def fill_days_data(data:dict, dates_dict:OrderedDict, profile:models.Profile):
    for k, v in data.items():
        v['date'] = v['food_log_date'] or v['daily_log_date']
        v['user_activity_level'] = v['user_activity_level'] if v['user_activity_level'] else profile.activity_level
        dates_dict[k] = Day(**v)
    
    return dates_dict

async def transform_daily(profile:models.Profile, data:dict, end_date:date=date.today()):
    dates_dict = create_dictionary_of_days(start_date=profile.start_date, end_date=end_date)
    dates_dict = fill_days_data(data=data, dates_dict=dates_dict, profile=profile)

    # set starting calcs
    est_weight = profile.start_weight
    total_calorie_goal = 0
    total_calories_eaten = 0
    total_rmr = 0

    # create overview log of all dates
    logs = []
    for v in dates_dict.values():
        log = Log(day=v, profile=profile, est_weight=est_weight, total_calorie_goal=total_calorie_goal, total_calories_eaten=total_calories_eaten, total_rmr=total_rmr)

        logs.append(log.log())
        
        est_weight -= (log.resting_calories_burned()-v.calories_eaten_today)/3500
        total_calorie_goal = log.total_calorie_goal
        total_calories_eaten = log.total_calories_eaten
        total_rmr = log.total_rmr
    
    logs.reverse()
    return logs


async def daily_log(profile:models.Profile, db: Session, end_date=date.today()):

    if profile is None:
        raise ValueError("profile cannot be None")
 
    data = await get_aggregate_food_logs_and_actual_weight(profile, db)
    logs = await transform_daily(profile, data, end_date=end_date)
    
    return logs