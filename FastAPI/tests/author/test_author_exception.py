import pytest
import starlette.status

pytestmark = pytest.mark.asyncio


async def test_create_author_blank_name(async_client):
    response = await async_client.post("/authors", json={"name": " "})
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_author_too_long(async_client):
    response = await async_client.post("/authors", json={"name": "a" * 51})
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY
