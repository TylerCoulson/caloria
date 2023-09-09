from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # type: ignore
from datetime import date
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
async def get_food_logs(*, deps:LoggedInDeps, n:int=25, page:int=1):
    
    logs = await api_food_log.get_food_logs(n=n, page=page, profile=deps['profile'], db=deps['db'])
    
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": logs,
       }

    return templates.TemplateResponse("log/list.html", context)             

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
        "serving_amount": 1,
        "calories": 0,
    }

    if food_id:
        servings = await api_servings.get_serving_size_by_food(food_id=food_id, db=deps['db'])
        context['serving_id'] = serving_id
        context['food'] = await api_food.get_food_id(food_id=food_id, db=deps['db'])
        context['servings'] = servings['servings']
    
    if serving_id:
        current_serving = await api_servings.get_serving_size_id(serving_id=serving_id, db=deps['db'])
        food = current_serving.food
        servings = await api_servings.get_serving_size_by_food(food_id=food.id, db=deps['db'])
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
    
    
    log = await api_food_log.get_food_log_id(profile=deps['profile'], food_log_id=log_id, db=deps['db'])

    servings = await api_servings.get_serving_size_by_food(food_id=log.food_id, db=deps['db'])
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
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
async def get_food_log_id(*, deps:LoggedInDeps, food_log_id: int):
    
    
    log = await api_food_log.get_food_log_id(profile=deps['profile'], food_log_id=food_log_id, db=deps['db'])
    
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "log": log,
    }
    return templates.TemplateResponse("log/row.html", context)
    

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs_by_profile_date(*, deps:LoggedInDeps, n:int=25, page:int=1, date: date):

    
    logs = await api_food_log.get_food_log_date(n=n, page=page, date=date, profile=deps['profile'], db=deps['db'])
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
        return post_food_log(request=deps['request'], hx_request=deps['hx_request'], profile=deps['profile'], food_log=food_log_in, db=deps['db'])

    
    log = await api_food_log.update_food_log(food_log_id=food_log_id, food_log_in=food_log_in, profile=deps['profile'], db=deps['db'])

    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "log": log,
    }
    return templates.TemplateResponse("log/row.html", context)

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_food_log(*, deps:LoggedInDeps, food_log: schemas.FoodLogCreate):
    
    await api_food_log.post_food_log(profile=deps['profile'], food_log=food_log, db=deps['db'])
    logs = await api_food_log.get_food_logs(profile=deps['profile'], db=deps['db'])
    
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['profile'],
        "logs": logs,
    }
    return templates.TemplateResponse("log/list.html", context)             

@router.delete(
    "/{food_log_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food_log(*, deps:LoggedInDeps, food_log_id: int):
    
    await api_food_log.delete_food_log(food_log_id=food_log_id, profile=deps['profile'], db=deps['db'])

    return None
