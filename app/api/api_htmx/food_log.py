from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # type: ignore
from datetime import date
from app import deps
from app import schemas

from app.api.api_V1 import food_log as api_food_log
from app.api.api_V1 import food as api_food
from app.api.api_V1 import serving_size as api_servings
from app.api.api_htmx.deps import LoggedInDeps

router = APIRouter(prefix="/food_log")
templates = Jinja2Templates("app/templates")


@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs(*, logged_in:LoggedInDeps, n:int=25, page:int=1):
    
    logs = await api_food_log.get_food_logs(n=n, page=page, profile=logged_in['profile'], db=logged_in['db'])
    
    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "logs": logs,
       }

    return templates.TemplateResponse("log/list.html", context)             

@router.get(
    "/create",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_create_log(*, logged_in:LoggedInDeps, food_id:int=None, serving_id:int=None):

    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "serving_amount": 1,
        "calories": 0,
    }

    if food_id:
        servings = await api_servings.get_serving_size_by_food(food_id=food_id, db=logged_in['db'])
        context['serving_id'] = serving_id
        context['food'] = await api_food.get_food_id(food_id=food_id, db=logged_in['db'])
        context['servings'] = servings['servings']
    
    if serving_id:
        current_serving = await api_servings.get_serving_size_id(serving_id=serving_id, db=logged_in['db'])
        food = current_serving.food
        servings = await api_servings.get_serving_size_by_food(food_id=food.id, db=logged_in['db'])
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
async def get_log_edit(*, logged_in:LoggedInDeps, log_id:int, copy:bool = False):
    
    
    log = await api_food_log.get_food_log_id(profile=logged_in['profile'], food_log_id=log_id, db=logged_in['db'])

    servings = await api_servings.get_serving_size_by_food(food_id=log.food_id, db=logged_in['db'])
    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "trigger": 'click',
        "log":log,
        "editable": True,
        'servings': servings['servings'],
        'serving_id': log.serving_size_id,
        "serving_amount":log.serving_amount,
        "calories": log.serving_size.calories
    }

    if copy:
        context["log"].date = date.today()
        context["log"].id = 0
        context['editable'] = False

        return templates.TemplateResponse("log/inputs/edit/copy.html", context)
    
    return templates.TemplateResponse("log/inputs/edit/edit.html", context)


@router.get(
    "/{food_log_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_log_id(*, logged_in:LoggedInDeps, food_log_id: int):
    
    
    log = await api_food_log.get_food_log_id(profile=logged_in['profile'], food_log_id=food_log_id, db=logged_in['db'])
    
    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "log": log,
    }
    return templates.TemplateResponse("log/row.html", context)
    

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs_by_profile_date(*, logged_in:LoggedInDeps, n:int=25, page:int=1, date: date):

    
    logs = await api_food_log.get_food_log_date(n=n, page=page, date=date, profile=logged_in['profile'], db=logged_in['db'])
    logs = logs['log']
    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "logs": logs,
        "trigger": 'click'
    }
    
    return templates.TemplateResponse("log/day.html", context)



@router.put(
    "/{food_log_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_food_log(*, logged_in:LoggedInDeps, food_log_id: int, food_log_in: schemas.FoodLogBase):
    

    if food_log_id == 0:
        return post_food_log(request=logged_in['request'], hx_request=logged_in['hx_request'], profile=logged_in['profile'], food_log=food_log_in, db=logged_in['db'])

    
    log = await api_food_log.update_food_log(food_log_id=food_log_id, food_log_in=food_log_in, profile=logged_in['profile'], db=logged_in['db'])

    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "log": log,
    }
    return templates.TemplateResponse("log/row.html", context)

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_food_log(*, logged_in:LoggedInDeps, food_log: schemas.FoodLogCreate):
    
    await api_food_log.post_food_log(profile=logged_in['profile'], food_log=food_log, db=logged_in['db'])
    logs = await api_food_log.get_food_logs(profile=logged_in['profile'], db=logged_in['db'])
    
    context = {
        "request": logged_in['request'],
        "hx_request": logged_in['hx_request'],
        "user": logged_in['profile'],
        "logs": logs,
    }
    return templates.TemplateResponse("log/list.html", context)             

@router.delete(
    "/{food_log_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food_log(*, logged_in:LoggedInDeps, food_log_id: int):
    
    await api_food_log.delete_food_log(food_log_id=food_log_id, profile=logged_in['profile'], db=logged_in['db'])

    return None
