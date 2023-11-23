from app.api.api_V1.deps import CommonDeps, LoggedInDeps
from app.api.api_V1 import daily_overview as api_daily

async def calorie_progress_data(deps:LoggedInDeps, overview=None, total:bool=False):
    """
    overview - Data for the current day 
    total - Use totals amounts from all days
    """
    if overview is None:
        overview = await api_daily.get_daily(deps=deps, current_date=deps['client_date'])
    
    if total:
        pass

    offsets = {
            "calorie_info": {
                "calories_burned":overview['calories_burned'],
                "calories_eaten":overview['eaten_calories'],
                "calorie_goal":overview['calorie_goal'],
            },
            "white_offset_max": ((1 - (overview['calorie_goal']/overview['calories_burned']))),
            "white_offset": 
            max(
                ((1 - min(overview['eaten_calories']/overview['calories_burned'], 1))),
                ((1 - (overview['calorie_goal']/overview['calories_burned'])))
            ),
            "yellow_offset":  ((1 - min(overview['eaten_calories']/overview['calories_burned'], 1))),
            "red_offset":
                (
                    (
                        1 - (
                            min(
                                overview['eaten_calories']/overview['calories_burned'] - 1,
                                1
                            )
                        )
                    )
                ), 
        }
    return offsets