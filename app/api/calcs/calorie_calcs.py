from datetime import date, timedelta


class PersonsDay():
    '''
    height - inches
    start_weight - lbs
    sex - male or female
    goal_weight - lbs
    '''
    def __init__(self, height:int, start_weight:float, start_date:date, lbs_per_day:float, birthdate:date, sex:str, activity_level:float, goal_weight:float, profile_logs:list) -> None:
        self.height = height
        self.start_weight = start_weight
        self.start_date = start_date
        self.lbs_per_day = lbs_per_day
        self.birthdate = birthdate
        self.sex = sex
        self.activity_level = activity_level
        self.goal_weight = goal_weight
        self.profile_logs = profile_logs
        self.lowest_allowed = 1200 if sex == 'female' else 1500

    def check_possible(self):
        if self.goal_weight > self.start_weight:
            return "Goal Weight greater than Start Weight"
        
        if self.resting_rate(self.goal_weight, self.age(current_date=self.start_date)) < self.lowest_allowed:
            return "Goal weight resting calories are less than lowest allowed calories"
    
        return True

    def bmi(self, current_date:date):
        est_weight = self.estimated_weight(current_date=current_date, total_calories_eaten=self.total_calories_eaten(current_date=current_date))
        return round((est_weight/(self.height**2))*703,2)


    def total_calories_eaten(self, current_date:date):

        total_calories_eaten = 0 
        # need to use a join on the logs to fix this.
        for log in self.profile_logs:
            if log.date <= current_date and log.date >= self.start_date:
                calories = log.serving_amount * log.serving_size.calories
                total_calories_eaten += calories
            else:
                pass
        return int(round(total_calories_eaten,0))

    def estimated_weight(self, current_date:date, total_calories_eaten:int=None):
        if total_calories_eaten is None:
            total_calories_eaten = self.total_calories_eaten(current_date=current_date)

        start_rmr = self.resting_rate(weight=self.start_weight, age=self.age(current_date=self.start_date))

        days = (current_date - self.start_date).days

        current_age = self.age(current_date)
        ideal_lbs_lost = (self.lbs_per_day * days)

        ideal_weight = max(round(self.start_weight - ideal_lbs_lost,1), self.goal_weight)
        ideal_rmr = self.resting_rate(weight=ideal_weight, age=current_age)
        average_rmr = (ideal_rmr+start_rmr)/2

        total_ideal_calories = average_rmr * days
        
        net_calories = total_ideal_calories - total_calories_eaten
        
        est_weight = self.start_weight - (net_calories/3500)
        return round(est_weight,1)

    def calories_eaten_on_date(self, current_date:date):
        calories_eaten_on_current_date = 0 
        # need to use a join on the logs to fix this.
        for log in self.profile_logs:
            if log.date == current_date:
                calories = log.serving_amount * log.serving_size.calories
                calories_eaten_on_current_date += calories
            else:
                continue
        return int(round(calories_eaten_on_current_date,0))

    def calorie_goal(self, weight:float, age:float):
        rmr = self.resting_rate(weight=weight, age=age)

        if weight > self.goal_weight:
            calorie_goal = max(rmr - ((self.lbs_per_day*7) * 500), self.lowest_allowed) 
        else:
            calorie_goal = rmr

        return int(round(calorie_goal,0))

    def total_lbs_lost(self, current_date:date):
        return round(self.start_weight - self.estimated_weight(current_date=current_date), 1)
        
    def calorie_surplus(self, current_date:date):
        start_age = self.age(current_date=self.birthdate)
        est_weight = self.estimated_weight(current_date=current_date)
        current_age = self.age(current_date=current_date)

        start_goal = self.calorie_goal(weight=self.start_weight, age=start_age)
        est_goal = self.calorie_goal(weight=est_weight, age=current_age)
        
        cal_goal = (start_goal + est_goal)/2
        total_calorie_goal = cal_goal * (current_date - self.start_date).days

        total_calories_eaten = total_calorie_goal - self.total_calories_eaten(current_date=current_date) 
        
        return int(round(total_calories_eaten,0))

    def age(self, current_date:date):

        years = current_date.year - self.birthdate.year - (1 if ((current_date.month, current_date.day) < (self.birthdate.month, self.birthdate.day)) else 0)

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
        return int(round(resting_rate))

    def prediction(self):
        """
        This method returns a dictionary of predicted daily values of every day until goal weight is acheived.
        It assumes the person exactly sticks to the calorie goal 
        It has a maximum output of 10 years of predicted days.
        It only gives returns from the start date till the goal has been met or 10 years has been reached
        """
        total_calories_eaten = 0
        output = {}
        est_weight = self.start_weight
        day = 0
        start_age = self.start_date.year - self.birthdate.year - (1 if ((self.start_date.month, self.start_date.day) < (self.birthdate.month, self.birthdate.day)) else 0)
        prior_weight = est_weight
        rest_rate = self.resting_rate(weight=est_weight, age=start_age)
        net_calories = self.calorie_goal(weight=est_weight, age=start_age)
        bmi = round((est_weight/(self.height**2))*703,2)

        output = {'0':{
                "day": day+1,
                "week": day//7 + 1,
                "date": self.start_date.isoformat(),
                "est_weight": round(est_weight,1),
                "resting_rate": rest_rate,
                "net_calories": net_calories,
                "total_lbs_lost": round(self.start_weight - est_weight, 1),
                "lbs_lost_today": round(prior_weight - est_weight, 2),
                "bmi": bmi}}

        while True:
            if (day>=3652) or (self.goal_weight >= est_weight):
                break

            current_date = self.start_date + timedelta(day)     
            age = self.age(current_date=current_date)
            est_weight = prior_weight - ((rest_rate - net_calories)/3500)
            rest_rate = self.resting_rate(weight=est_weight, age=age)
            net_calories = self.calorie_goal(weight=est_weight, age=age)
            bmi = round((est_weight/(self.height**2))*703,2)
            
            output[f'{day+1}'] = {
                "day": day+2,
                "week": day//7 + 1,
                "date": (current_date+ timedelta(1)).isoformat(),
                "est_weight": round(est_weight,1),
                "resting_rate": rest_rate,
                "net_calories": net_calories,
                "total_lbs_lost": round(self.start_weight - est_weight, 1),
                "lbs_lost_today": round(prior_weight - est_weight, 2),
                "bmi": bmi
            }
            prior_weight = est_weight
            total_calories_eaten += net_calories
            day += 1
    
        return output