from sqlalchemy import select
from app import models

async def test_food_log_update(client, update_log):
    update_log["serving_amount"] = 5
    response = await client.put(f"/api/v1/food_log/{update_log['id']}", json=update_log)

    assert response.status_code == 200
    
    content = response.json()

    assert "serving_size" in content
    for key, value in update_log.items():
        assert content[key] == value

async def test_food_log_update_wrong_profile_id(client, db, update_wrong_profile_log):
    response = await client.put(f"/api/v1/food_log/{update_wrong_profile_log['id']}", json=update_wrong_profile_log)

    assert response.status_code == 404

    statement = select(models.Food_Log).where(models.Food_Log.id == update_wrong_profile_log['id'])
    data = await db.execute(statement)
    results = data.unique().scalar_one_or_none()

    for i in update_wrong_profile_log:
        att = getattr(results, i)
        if i == "date":
            att = att.strftime('%Y-%m-%d')
        assert att == update_wrong_profile_log[i]
    