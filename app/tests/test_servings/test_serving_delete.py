delete_id = 22
invalid_id = "abc"

async def test_delete_serving_size_valid_food_id_serving_id(client) -> None:

    # Perform the delete request
    response = await client.delete(f"api/v1/food/{delete_id}/serving/{delete_id}")

    # Assert that the delete request was successful
    assert response.status_code == 200

async def test_delete_serving_size_invalid_food_id(client) -> None:
    # Perform the delete request
    response = await client.delete(f"api/v1/food/{invalid_id}/serving/{delete_id}")

    # Assert that the delete request returns a 404 error code
    assert response.status_code == 422

async def test_delete_serving_size_invalid_serving_id(client) -> None:

    # Perform the delete request
    response = await client.delete(f"api/v1/food/{delete_id}/serving/{invalid_id}")

    # Assert that the delete request returns a 404 error code
    assert response.status_code == 422

async def test_delete_nonexistent_serving_size(client):
    #  Deleting a serving size that does not exist
    response = await client.delete("api/v1/food/1/serving/9999")
    assert response.status_code == 404