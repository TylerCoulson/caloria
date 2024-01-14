async def test_food_log_read_day(client, get_date_logs):
    response= await client.get(f"/api/v1/food_log/date/{get_date_logs[0]['date']}")

    assert response.status_code == 200
    content = response.json()

    for log in content['log']:
        assert "serving_size" in log
        log.pop('serving_size')
        assert log in get_date_logs