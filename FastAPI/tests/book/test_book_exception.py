import pytest
import starlette.status

pytestmark = pytest.mark.asyncio


async def _create_author(async_client, name="Test Author"):
    response = await async_client.post("/authors", json={"name": name})
    assert response.status_code == starlette.status.HTTP_201_CREATED
    return response.json()["id"]


async def test_create_book_blank_title(async_client):
    author_id = await _create_author(async_client)
    response = await async_client.post(
        "/books", json={"title": " ", "author_id": author_id}
    )
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_book_invalid_author_id(async_client):
    response = await async_client.post(
        "/books",
        json={"title": "Ghost Book", "author_id": "11111111-1111-1111-1111-111111111111"},
    )
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST


async def test_delete_book_not_found(async_client):
    response = await async_client.delete(
        "/books/11111111-1111-1111-1111-111111111111"
    )
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
