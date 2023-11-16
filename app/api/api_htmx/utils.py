from app.api.api_V1.deps import CommonDeps, LoggedInDeps
from app.api.api_V1 import daily_overview as api_daily

async def calorie_progress_data(deps:LoggedInDeps, overview=None):
    if overview is None:
        overview = await api_daily.get_daily(deps=deps, current_date=deps['client_date'])
    
    circumference = 326.7256
    offsets = {
            "circumference": circumference,
            "white_offset_max": ((1 - (overview['calorie_goal']/overview['calories_burned'])) * circumference),
            "white_offset": 
            max(
                ((1 - min(overview['eaten_calories']/overview['calories_burned'], 1)) * circumference),
                ((1 - (overview['calorie_goal']/overview['calories_burned'])) * circumference)
            ),
            "yellow_offset":  ((1 - min(overview['eaten_calories']/overview['calories_burned'], 1)) * circumference),
            "red_offset": min(
                (
                    (
                        1 - (
                            min(
                                overview['eaten_calories']/overview['calories_burned'] - 1,
                                1
                            )
                        )
                    ) * circumference
                ), 
                circumference),
        }
    return offsets