from app.api.api_V1.deps import CommonDeps, LoggedInDeps
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

    offsets = {
            "calorie_info": {
                "calories_burned":calories_burned,
                "calories_eaten":calories_eaten,
                "calorie_goal":calorie_goal,
            },
            "white_offset_max": ((1 - (calorie_goal/calories_burned))),
            "white_offset": 
            max(
                ((1 - min(calories_eaten/calories_burned, 1))),
                ((1 - (calorie_goal/calories_burned)))
            ),
            "yellow_offset":  ((1 - min(calories_eaten/calories_burned, 1))),
            "red_offset":
                (
                    (
                        1 - (
                            min(
                                calories_eaten/calories_burned - 1,
                                1
                            )
                        )
                    )
                ), 
        }
    return offsets