from app.api.api_htmx.deps import CommonDeps, LoggedInDeps
from app.api.api_V1 import daily_overview as api_daily

async def calorie_progress_data(deps:LoggedInDeps, overview=None, total:bool=False):
    """
    overview - Data for the current day 
    total - Use totals amounts from all days
    """
    if overview is None:
        overview = await api_daily.get_daily(deps=deps, current_date=deps['client_date'])
    
    calories_burned = overview['calories_burned']
    calories_eaten = overview['eaten_calories']
    calorie_goal = overview['calorie_goal']

    if total:
        calories_burned = overview['total_calories_burned']
        calories_eaten = overview['total_calories_eaten']
        calorie_goal = overview['total_calorie_goal']

    goal_to_burn = calorie_goal/calories_burned
    offsets = {
            "calorie_info": {
                "calories_burned":calories_burned,
                "calories_eaten":calories_eaten,
                "calorie_goal":calorie_goal,
            },
            "goal_rotation": (goal_to_burn) * 360 ,
            "max_eaten":goal_to_burn,
            "max_goal": (calories_burned - calorie_goal) / calories_burned,
            "eaten_percentage": min(
                                    (calories_eaten/calories_burned),
                                    goal_to_burn
                                ),
            "over_goal_percentage":  min(
                                        max(calories_eaten - calorie_goal, 0) / calories_burned,
                                        (calories_burned - calorie_goal) / calories_burned
                                    ),
            "over_rmr_percentage": min(
                                        max((calories_eaten/calories_burned - 1), 0),
                                        1
                                    ), 
        }
    return offsets