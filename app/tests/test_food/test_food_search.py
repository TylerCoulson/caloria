async def test_get_food_search_search_word_exists_in_type(client):
    response = await client.get("/api/v1/food/search?search_word=posuere")
    assert response.status_code == 200
    assert len(response.json()) > 0

async def test_get_food_search_search_word_exists_in_subtype(client):
    response = await client.get("/api/v1/food/search?search_word=dapibus")
    assert response.status_code == 200
    assert len(response.json()) > 0

async def test_get_food_search_search_word_not_exists(client):
    response = await client.get("/api/v1/food/search?search_word=xyz")
    assert response.status_code == 200
    assert len(response.json()) == 0

async def test_get_food_search_limit_and_offset_parameters(client):
    response = await client.get("/api/v1/food/search?search_word=posuere&n=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) > 0