import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.tests.test_htmx.htmx_utils import methods

@pytest.mark.parametrize(
        "url",
        methods['DELETE']
)
async def test_delete(client:TestClient, db:Session, url):
    response = await client.delete(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"