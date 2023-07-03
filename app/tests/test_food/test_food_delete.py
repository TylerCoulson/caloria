async def test_delete_existing_food(client, delete_food):
    # Test case: Deleting an existing food item
    response = await client.delete(f"/api/v1/food/{delete_food['id']}")
    assert response.status_code == 200


async def test_delete_non_existing_food(client):
    # Test case: Deleting a non-existing food item
    response = await client.delete("/api/v1/food/9999")
    assert response.status_code == 404
    assert "detail" in response.json()


async def test_delete_food_with_invalid_id(client):
    # Test case: Deleting a food item with invalid ID
    response = await client.delete("/api/v1/food/abc")
    assert response.status_code == 422
    assert "detail" in response.json()