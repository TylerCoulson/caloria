async def test_food_log_read_id(client, get_date_logs):
    response= await client.get(f"/api/v1/food_log/{get_date_logs[0]['id']}")

    assert response.status_code == 200
    content = response.json()

    for key, value in get_date_logs[0].items():
        assert content[key] == value