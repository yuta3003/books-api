import pytest
import starlette.status

pytestmark = pytest.mark.asyncio


async def _create_author(async_client, name="Test Author"):
    response = await async_client.post("/authors", json={"name": name})
    assert response.status_code == starlette.status.HTTP_201_CREATED
    return response.json()["id"]


async def test_list_books_empty(async_client):
    response = await async_client.get("/books")
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json() == []


async def test_create_book(async_client):
    author_id = await _create_author(async_client)
    response = await async_client.post(
        "/books", json={"title": "No Longer Human", "author_id": author_id}
    )
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response_obj = response.json()
    assert response_obj["title"] == "No Longer Human"
    assert response_obj["author_id"] == author_id
    assert isinstance(response_obj["id"], str)

    response = await async_client.get("/books")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "No Longer Human"


async def test_list_books_ordered(async_client):
    author_id = await _create_author(async_client)
    await async_client.post(
        "/books", json={"title": "B Title", "author_id": author_id}
    )
    await async_client.post(
        "/books", json={"title": "A Title", "author_id": author_id}
    )

    response = await async_client.get("/books")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert [item["title"] for item in response_obj] == ["A Title", "B Title"]


async def test_delete_book(async_client):
    author_id = await _create_author(async_client)
    response = await async_client.post(
        "/books", json={"title": "Delete Me", "author_id": author_id}
    )
    book_id = response.json()["id"]

    response = await async_client.delete(f"/books/{book_id}")
    assert response.status_code == starlette.status.HTTP_204_NO_CONTENT

    response = await async_client.get("/books")
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json() == []
