from datetime import date

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