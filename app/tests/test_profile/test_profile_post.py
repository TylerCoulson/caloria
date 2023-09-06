async def test_successful_profile_creation(client, create_profile):
    response = await client.post( "/api/v1/profile", json=create_profile)
    assert response.status_code == 201
    assert response.json() == create_profile


async def test_invalid_input(client):
    response = await client.post( "/api/v1/profile", json={"profile": { "name": "John Doe", "age": "twenty-five", "email": "johndoe@example.com"}},
    )
    assert response.status_code == 422
    assert "detail" in response.json()