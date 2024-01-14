# async def test_daily_overview_delete_by_date(client, db):    
#     end_date = "2023-12-07"

#     daily = {
#         "profile_id": 1,
#         "date": end_date,
#         "actual_weight": 308.8
#     }
#     data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=temp_profile)


#     response= await client.delete(f"/api/v1/daily/{data.date}")
#     assert response.status_code == 200

#     assert response.json() is None

#     assert await crud.read(_id=data.id, db=db, model=models.DailyLog)  is None

# async def test_daily_overview_delete_by_id(client:TestClient, db:Session):    
#     end_date = "2023-12-07"

#     daily = {
#         "profile_id": 1,
#         "date": end_date,
#         "actual_weight": 308.8
#     }
#     data = await crud.create(obj_in=schemas.DailyOverviewInput(**daily), db=db, model=models.DailyLog, profile=temp_profile)


#     response= await client.delete(f"/api/v1/daily/{data.id}")
#     assert response.status_code == 200

#     assert response.json() is None

#     assert await crud.read(_id=data.id, db=db, model=models.DailyLog)  is None