from datetime import date as t_date, datetime
from app import schemas

class Day():
    def __init__(self, date:t_date, calories_eaten_today:int=0, fats_eaten_today:int=0, carbs_eaten_today:int=0, protein_eaten_today:int=0, user_inputed_weight:float=0, user_activity_level:float=0, **kwargs) -> None:
        self.date = date
        self.calories_eaten_today = calories_eaten_today
        self.fats_eaten_today = fats_eaten_today
        self.carbs_eaten_today = carbs_eaten_today
        self.protein_eaten_today = protein_eaten_today
        self.user_inputed_weight = user_inputed_weight
        self.user_activity_level = user_activity_level

        
class Log():
    def __init__(self,
                day: Day,
                profile: schemas.Profile,
                est_weight,
                total_calorie_goal,
                total_calories_eaten,
                total_rmr
                ) -> None:
        self.day = day
        self.profile = profile
        self.est_weight = est_weight
        self.total_calorie_goal = total_calorie_goal
        self.total_calories_eaten = total_calories_eaten
        self.total_rmr = total_rmr

    def resting_calories_burned(self):

        weight_calc = 10 * (self.est_weight/2.2)
        sex_calc = -161 if self.profile.sex == 'female' else 5
        height_calc = (self.profile.height*2.54) * 6.25
        age_calc = int((self.day.date - self.profile.birthdate).days/365.25) * 5

        return round(((weight_calc+height_calc-age_calc) + sex_calc) * self.day.user_activity_level,0)
    



    def log(self):
        day = (self.day.date - self.profile.start_date).days +1 

        calorie_goal = max(self.resting_calories_burned() - self.profile.lbs_per_week * 500, 1200 if self.profile.sex == 'female' else 1500)

        self.total_rmr += self.resting_calories_burned()
        self.total_calories_eaten += self.day.calories_eaten_today
        self.total_calorie_goal += calorie_goal

        log = {
            "date": self.day.date,
            "profile_id": self.profile.id,
            'day':day,
            'week':((day-1)//7)+1,
            'est_weight':round(self.est_weight,1),
            'calories_burned':self.resting_calories_burned(),
            'eaten_calories':round(self.day.calories_eaten_today,0),
            'eaten_fats':round(self.day.fats_eaten_today,0),
            'eaten_carbs':round(self.day.carbs_eaten_today,0),
            'eaten_protein':round(self.day.protein_eaten_today,0),
            'calorie_goal': round(calorie_goal,0),
            'total_lbs_lost':round((self.total_rmr - self.total_calories_eaten)/3500,2),
            'calorie_surplus': round(self.total_calorie_goal - self.total_calories_eaten,0),
            'calories_left':round(calorie_goal - self.day.calories_eaten_today,0),
            'bmi':round((self.est_weight/float(self.profile.height**2))*703,2),
            'actual_weight': self.day.user_inputed_weight or 0,
            'activity_level': self.day.user_activity_level
        }

        return log