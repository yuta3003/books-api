import pytest
import starlette.status

pytestmark = pytest.mark.asyncio


async def test_list_authors_empty(async_client):
    response = await async_client.get("/authors")
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json() == []


async def test_create_author(async_client):
    response = await async_client.post("/authors", json={"name": "Osamu Dazai"})
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response_obj = response.json()
    assert response_obj["name"] == "Osamu Dazai"
    assert isinstance(response_obj["id"], str)

    response = await async_client.get("/authors")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["name"] == "Osamu Dazai"


async def test_list_authors_ordered(async_client):
    await async_client.post("/authors", json={"name": "B Author"})
    await async_client.post("/authors", json={"name": "A Author"})

    response = await async_client.get("/authors")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert [item["name"] for item in response_obj] == ["A Author", "B Author"]
