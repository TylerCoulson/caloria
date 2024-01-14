import pytest


@pytest.fixture()
async def create_log():
    log = {"id":1001, "date":'2022-12-09', "food_id":123, "serving_size_id":123, "serving_amount":3, "profile_id":1}
    return log

@pytest.fixture()
async def get_date_logs():
    get_log = [{ "id":12, "date":'2022-10-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1,}, { "id":97, "date":'2022-10-09', "food_id":813, "serving_size_id":813, "serving_amount":9.0, "profile_id":1,}, { "id":429, "date":'2022-10-09', "food_id":426, "serving_size_id":426, "serving_amount":85.0, "profile_id":1,}, { "id":713, "date":'2022-10-09', "food_id":571, "serving_size_id":571, "serving_amount":25.0, "profile_id":1, }]
    return get_log

@pytest.fixture()
async def update_log():
    update_data = {"id":17, "date":'2023-04-27', "food_id":123, "serving_size_id":123, "serving_amount":4.0, "profile_id":1}
    return update_data

@pytest.fixture()
async def update_wrong_profile_log():
    update_data = {"id":20, "date":'2022-12-15', "food_id":246, "serving_size_id":246, "serving_amount":17, "profile_id":3}
    return update_data


@pytest.fixture()
async def delete_log():
    delete_data = {"id":18, "date":'2022-10-10', "food_id":780, "serving_size_id":780, "serving_amount":42, "profile_id":1}
    return delete_data

@pytest.fixture()
async def delete_wrong_profile_log():
    delete_data = {"id":19, "date":'2022-08-23', "food_id":9, "serving_size_id":9, "serving_amount":3, "profile_id":3}
    return delete_data