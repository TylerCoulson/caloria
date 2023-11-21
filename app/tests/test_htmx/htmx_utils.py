import re
from app.main import app
from datetime import date
import pytest

weight_params = {"height":70, "start_weight":320, "start_date":date(2023,7,12), "lbs_per_week":2, "birthdate":date(1992,12,5), "sex":"male", "activity_level":1.2, "goal_weight":150}

def _methods():
    data = {
        "{date": date(2023,12,6),
        "{food_id": 1,
        "{food_type": 'posuere',
        "{food_log_id": 1
    }

    def re_path(path) -> str:
        sub_paths = path.split("/")
        new_path = []
        for i in sub_paths:
            try:
                match = re.search("{\w+", i)
                i = str(data[match.group(0)])
                
            except:
                pass
            new_path.append(i)
        
        return "/".join(new_path)

    # Get all paths and sort into methods
    methods = {"POST":[],"GET":[],"PUT":[],"DELETE":[]}
    for route in app.router.__dict__["routes"]:
        if hasattr(route, "tags"):
            if "htmx" in route.__dict__["tags"]:
                for method in route.__dict__["methods"]:
                    new_path = re_path(route.__dict__["path"])
                    
                    methods[method].append(new_path)
            else:
                pass

    return methods

methods = _methods()