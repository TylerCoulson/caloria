from datetime import date


class PersonsDay():
    '''
    height - inches
    start_weight - lbs
    sex - male or female
    goal_weight - lbs
    '''
    def __init__(self, height, start_weight, start_date, lbs_per_day, birthdate, sex, activity_level, goal_weight, user_logs, current_date) -> None:
        self.height:int = height
        self.start_weight:float = start_weight
        self.start_date:date = start_date
        self.lbs_per_day:float = lbs_per_day
        self.birthdate:date = birthdate
        self.sex:str = sex
        self.activity_level:float = activity_level
        self.goal_weight:float = goal_weight
        self.user_logs:list = user_logs
        self.current_date = current_date


    def bmi(self):
        return round((self.estimated_weight()/(self.height**2))*703,2)


    def total_calories_eaten(self):

        total_calories_eaten = 0 
        # need to use a join on the logs to fix this.
        for log in self.user_logs:
            if log.date < self.current_date and log.date >= self.start_date:
                calories = log.serving_amount * log.serving_size.calories
                total_calories_eaten += calories
            else:
                pass
        return round(total_calories_eaten,0)

    def estimated_weight(self):
        start_rmr = self.resting_rate(self.start_weight, self.age(current_date=self.birthdate))

        days = (self.current_date - self.start_date).days

        current_age = self.age(self.current_date) 
        ideal_weight = round(self.start_weight - (self.lbs_per_day * days),1)
        ideal_rmr = self.resting_rate(weight=ideal_weight, age=current_age)
        average_rmr = (ideal_rmr+start_rmr)/2

        total_ideal_calories = average_rmr * days

        net_calories = total_ideal_calories - self.total_calories_eaten() 

        est_weight = self.start_weight - (net_calories/3500)
        return round(est_weight,1)

    def calories_eaten_today(self):
        calories_eaten_on_current_date = 0 
        # need to use a join on the logs to fix this.
        for log in self.user_logs:
            if log.date == date:
                calories = log.serving_amount * log.serving_size.calories
                calories_eaten_on_current_date += calories
            else:
                continue
        
        return round(calories_eaten_on_current_date,0)

    def calorie_goal(self, weight:float, age:float):
        lowest_allowed = 1200 if self.sex == 'female' else 1500

        rmr = self.resting_rate(weight=weight, age=age)
        
        if weight > self.goal_weight:
            calorie_goal = max(rmr - ((self.lbs_per_day*7) * 500), lowest_allowed) 
        else:
            calorie_goal = rmr

        return round(calorie_goal,0)

    def total_lbs_lost(self):
        return round(self.start_weight - self.estimated_weight(), 1)
        
    def calorie_surplus(self):
        start_age = self.age(current_date=self.birthdate)
        est_weight = self.estimated_weight()
        current_age = self.age(current_date=self.current_date)

        start_goal = self.calorie_goal(weight=self.start_weight, age=start_age)
        est_goal = self.calorie_goal(weight=est_weight, age=current_age)
        
        cal_goal = (start_goal + est_goal)/2
        total_calorie_goal = cal_goal * (self.current_date - self.start_date).days

        total_calories_eaten = total_calorie_goal - self.total_calories_eaten() 
        
        return round(total_calories_eaten,0)

    def age(self, current_date:date):
        print("START")
        years = current_date.year - self.birthdate.year - (1 if ((current_date.month, current_date.day) < (self.birthdate.month, self.birthdate.day)) else 0)
        print("ETERE")
        return years

    def resting_rate(self, weight:float, age:int):
        '''Calculates resting metabolic rate
        weight in lbs
        height in inches
        '''
        
        weight_calc = 10*(weight/2.2)
        height_calc = 6.25*(self.height*2.54)
        age_calc = (5*age)
        gender_calc = -161 if self.sex == 'female' else 5

        resting_rate = ( (weight_calc+height_calc-age_calc) + gender_calc) * self.activity_level
        return round(resting_rate)