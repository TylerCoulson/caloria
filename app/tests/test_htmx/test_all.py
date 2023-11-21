import re
from app.main import app
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from datetime import date

weight_params = {"height":70, "start_weight":320, "start_date":date(2023,7,12), "lbs_per_week":2, "birthdate":date(1992,12,5), "sex":"male", "activity_level":1.2, "goal_weight":150}
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

@pytest.mark.parametrize(
        "url",
        methods['GET']
)
async def test_gets(client:TestClient, db:Session, url):
    params = {"food_category": 1, "search_word":"test", "food_id":1, "log_id":1, **weight_params, "email":"test123@test.com","password":"1231412321", "password_confirm":"1231412321"}
    response = await client.get(url, params=params)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
