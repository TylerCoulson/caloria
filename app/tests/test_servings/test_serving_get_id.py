async def test_get_serving_size_id_successful(client, get_serving):
    response = await client.get(f"/api/v1/food/{get_serving['food_id']}/serving/{get_serving['id']}")
    assert response.status_code == 200
    assert response.json() == get_serving

async def test_get_serving_size_id_nonexistent(client, get_serving):
    response = await client.get(f"/api/v1/food/{get_serving['food_id']}/serving/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Serving size not found"}

async def test_get_serving_size_id_invalid_food_id(client):
    response = await client.get(f"/api/v1/food/abc/serving/1")
    assert response.status_code == 422


async def test_get_serving_size_id_invalid_serving_id(client, get_serving):
    response = await client.get(f"/api/v1/food/{get_serving['food_id']}/serving/abc")
    assert response.status_code == 422


async def test_get_serving_size_id_missing_food_id(client):
    response = await client.get(f"/api/v1/food//serving/1")
    assert response.status_code == 404


async def test_get_serving_size_id_missing_serving_id(client, get_serving):
    response = await client.get(f"/api/v1/food/{get_serving['food_id']}/serving/")

    assert response.status_code == 307