from datetime import date


def bmi(height: float, weight:float):
    return round((weight/(height**2))*703,2)

def days_between(start_date:date, end_date:date):
    return (end_date - start_date).days


def total_calories_eaten(logs:list, date:date, start_date:date):
    total_calories_eaten = 0 
    # need to use a join on the logs to fix this.
    for log in logs:
        if log.date < date and log.date >= start_date:
            calories = log.serving_amount * log.serving_size.calories
            total_calories_eaten += calories
        else:
            pass
    return round(total_calories_eaten,0)

def estimated_weight(total_calories_eaten:int, start_weight:float, lbs_per_day:float, days:int, start_age:int, current_age:int, height:int, sex:str, activity_level:float):
    start_rmr = resting_rate(weight=start_weight, height=height, age=start_age, sex=sex, activity_level=activity_level)

    ideal_weight = round(start_weight - (lbs_per_day * days),1)
    ideal_rmr = resting_rate(weight=ideal_weight, height=height, age=current_age, sex=sex, activity_level=activity_level)
    average_rmr = (ideal_rmr+start_rmr)/2

    total_ideal_calories = average_rmr * days

    net_calories = total_ideal_calories - total_calories_eaten 

    est_weight = start_weight - (net_calories/3500)
    return round(est_weight,1)

def calories_eaten(logs:list, date:date):
    calories_eaten_on_current_date = 0 
    # need to use a join on the logs to fix this.
    for log in logs:
        if log.date == date:
            calories = log.serving_amount * log.serving_size.calories
            calories_eaten_on_current_date += calories
        else:
            continue
    
    return round(calories_eaten_on_current_date,0)

def calorie_goal(est_weight:float, goal_weight:float, rmr:int, weekly_lbs_lose:float, sex:str):
    lowest_allowed = 1500 if sex == 'male' else 1200
    
    if est_weight > goal_weight:
            calorie_goal = max(rmr - (weekly_lbs_lose * 500), lowest_allowed) 
    else:
        calorie_goal = rmr

    return round(calorie_goal,0)

def total_lbs_lost(start_weight:float, est_weight:float):
    return round(start_weight - est_weight,1)
      
def calorie_surplus(start_weight:float, est_weight:float, cals_eatten:int, start_rmr:int, est_rmr:int, goal_weight:float, days:int, weekly_lbs_lose:float, sex:str):
    
    start_goal = calorie_goal(start_weight, goal_weight, start_rmr, weekly_lbs_lose, sex)
    est_goal = calorie_goal(est_weight, goal_weight, est_rmr, weekly_lbs_lose, sex)
    
    cal_goal = (start_goal + est_goal)/2
    total_calorie_goal = cal_goal * days

    total_calories_eaten = total_calorie_goal - cals_eatten 
    
    return round(total_calories_eaten,0)

def age(birthdate: date, current_date: date):
    years = current_date.year - birthdate.year - (1 if ((current_date.month, current_date.day) < (birthdate.month, birthdate.day)) else 0)
    return years

def resting_rate(weight:float, height:float, age:int, sex:str, activity_level:float) -> int:
    '''Calculates resting metabolic rate
    weight in lbs
    height in inches
    '''
    
    weight_calc = 10*(weight/2.2)
    height_calc = 6.25*(height*2.54)
    age_calc = (5*age)
    gender_calc = -161 if sex == 'female' else 5

    resting_rate = ( (weight_calc+height_calc-age_calc) + gender_calc) * activity_level
    return round(resting_rate)