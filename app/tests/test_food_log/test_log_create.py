async def test_food_log_create(client, create_log, module_profile):
    response = await client.post(f"/api/v1/food_log", json=create_log)
    assert response.status_code == 201
    content = response.json()
    print("content", content['profile'])
    print("module", module_profile)
    assert content['profile'] == module_profile
    assert "serving_size" in content
    for key in create_log.keys():
        assert content[key] == create_log[key]

async def test_food_log_create_wrong_profile_id(client, create_log):
    create_log["profile_id"] = 3
    response = await client.post(f"/api/v1/food_log", json=create_log)
    assert response.status_code == 201
    content = response.json()
    assert content['profile_id'] == 1