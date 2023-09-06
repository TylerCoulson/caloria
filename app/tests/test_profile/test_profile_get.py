async def test_get_profile_id_valid_id(client, get_profile):
    # Test if the function returns the expected data
    # when given a valid profile id
    response = await client.get("/api/v1/profile/me")
    assert response.status_code == 200
    assert response.json() == get_profile


async def test_get_profile_id_additional_properties(client, get_profile):
    # Test if the function returns the expected data
    # when given a profile with additional properties
    response = await client.get("/api/v1/profile/me", params={**get_profile, "alsk;dfj": 25})
    assert response.status_code == 200
    assert response.json() == get_profile