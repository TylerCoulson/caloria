from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from app import schemas

from app.api.api_V1 import food_log as api_food_log
from app.api.api_V1 import food as api_food
from app.api.api_V1 import serving_size as api_servings
from app.api.api_htmx.deps import LoggedInDeps

router = APIRouter(prefix="/food_log")
templates = Jinja2Templates("app/templates")


@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs(*, deps:LoggedInDeps, n:int=25, page:int=1, home:bool=False, appending:bool=False):
    
    logs = await api_food_log.get_food_logs(deps=deps, n=n, page=page)
    
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": logs,
        "home": home,
        "page":page,
        "appending": appending,
       }
    if appending:
        return templates.TemplateResponse("log/body.html", context)

    return templates.TemplateResponse("log/base.html", context)             

@router.get(
    "/create",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_create_log(*, deps:LoggedInDeps, food_id:int=None, serving_id:int=None):

    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "date": deps['client_date'],
        "serving_amount": 1,
        "calories": 0,
        "title": "Add Log"
    }

    if food_id:
        servings = await api_servings.get_serving_size_by_food(deps=deps, food_id=food_id)
        context['serving_id'] = serving_id
        context['food'] = await api_food.get_food_by_id(food_id=food_id, deps=deps)
        context['servings'] = servings['servings']
    
    if serving_id:
        current_serving = await api_servings.get_serving_size_by_id(serving_id=serving_id, deps=deps)
        food = current_serving.food
        servings = await api_servings.get_serving_size_by_food(food_id=food.id, deps=deps)
        context['serving_id'] = serving_id
        context['food'] = food
        context['servings'] = servings['servings']
        context['calories'] = current_serving.calories


    return templates.TemplateResponse("log/inputs/create.html", context)

@router.get(
    "/edit",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_log_edit(*, deps:LoggedInDeps, log_id:int, copy:bool = False):
    
    
    log = await api_food_log.get_food_log_id(food_log_id=log_id, deps=deps)

    servings = await api_servings.get_serving_size_by_food(food_id=log.food_id, deps=deps)
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "trigger": 'click',
        "date": log.date,
        "log":log,
        "editable": True,
        "food": log.serving_size.food,
        'servings': servings['servings'],
        'serving_id': log.serving_size_id,
        "serving_amount":log.serving_amount,
        "calories": log.serving_size.calories,
        "title": "Edit Log"
    }

    if copy:
        context["date"] = deps['client_date']
        context["log"].date = deps['client_date']
        context["log"].id = 0
        context['editable'] = False
        context["title"] = "Copy Log"
    
    return templates.TemplateResponse("log/inputs/create.html", context)


@router.get(
    "/{food_log_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_log_id(*, deps:LoggedInDeps, food_log_id: int):
    
    
    log = await api_food_log.get_food_log_id(food_log_id=food_log_id, deps=deps)
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": [log],
    }
    return templates.TemplateResponse("log/row.html", context)


@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs_by_profile_date(*, deps:LoggedInDeps, n:int=25, page:int=1, date: date):

    
    logs = await api_food_log.get_food_log_date(n=n, page=page, date=date, deps=deps)
    logs = logs['log']
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": logs,
        "trigger": 'click'
    }
    
    return templates.TemplateResponse("log/day.html", context)



@router.put(
    "/{food_log_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_food_log(*, deps:LoggedInDeps, food_log_id: int, food_log_in: schemas.FoodLogBase):
    

    if food_log_id == 0:
        return post_food_log(food_log=food_log_in, deps=deps)

    
    log = await api_food_log.update_food_log(food_log_id=food_log_id, food_log_in=food_log_in, deps=deps)

    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": [log],
    }
    return templates.TemplateResponse("log/row.html", context)

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_food_log(*, deps:LoggedInDeps, food_log: schemas.FoodLogCreate):
    
    await api_food_log.post_food_log(food_log=food_log, deps=deps)
    logs = await api_food_log.get_food_logs(deps=deps)
    
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": logs,
        "home": False,
        "page": 1,
    }
    return templates.TemplateResponse("log/base.html", context)             

@router.delete(
    "/{food_log_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food_log(*, deps:LoggedInDeps, food_log_id: int):
    
    await api_food_log.delete_food_log(food_log_id=food_log_id, deps=deps)

    return None
