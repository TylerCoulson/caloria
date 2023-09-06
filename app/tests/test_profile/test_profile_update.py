async def test_update_current_profile_successful(client, update_profile):
    # Test case: Successful update
    response = await client.put(
        "/api/v1/profile/me",
        json=update_profile,
    )
    assert response.status_code == 200
    assert response.json() == update_profile


async def test_update_current_profile_missing_field(client, ):
    # Test case: Update with missing required field
    response = await client.put("/api/v1/profile/me", json={},)
    assert response.status_code == 422
    assert "detail" in response.json()