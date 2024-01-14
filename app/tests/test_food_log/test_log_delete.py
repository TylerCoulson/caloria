from sqlalchemy import select
from app import models

async def test_food_log_delete(client, db, delete_log):
    response = await client.delete(f"/api/v1/food_log/{delete_log['id']}")

    assert response.status_code == 200
    assert response.json() is None

    statement = select(models.Food_Log).where(models.Food_Log.id == delete_log['id'])
    data = await db.execute(statement)
    assert data.unique().scalar_one_or_none() == None

async def test_food_log_delete_wrong_profile_id(client, db, delete_wrong_profile_log):
    response = await client.delete(f"/api/v1/food_log/{delete_wrong_profile_log['id']}")

    assert response.status_code == 404

    statement = select(models.Food_Log).where(models.Food_Log.id == delete_wrong_profile_log['id'])
    data = await db.execute(statement)
    results = data.unique().scalar_one_or_none()

    for i in delete_wrong_profile_log:
        att = getattr(results, i)
        if i == "date":
            att = att.strftime('%Y-%m-%d')
        assert att == delete_wrong_profile_log[i]