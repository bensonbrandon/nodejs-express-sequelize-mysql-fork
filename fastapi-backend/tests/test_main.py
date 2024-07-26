import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_tutorial():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
        response = await ac.post("/tutorials/", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Tutorial"
    assert response.json()["description"] == "Test Description"
    assert response.json()["published"] is True

@pytest.mark.asyncio
async def test_get_all_tutorials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tutorials/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_all_published_tutorials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tutorials/published")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_tutorial():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First, create a tutorial to ensure there is one to fetch
        payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
        create_response = await ac.post("/tutorials/", json=payload)
        tutorial_id = create_response.json()["id"]
        
        # Now, fetch the created tutorial
        response = await ac.get(f"/tutorials/{tutorial_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Tutorial"

@pytest.mark.asyncio
async def test_update_tutorial():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First, create a tutorial to ensure there is one to update
        payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
        create_response = await ac.post("/tutorials/", json=payload)
        tutorial_id = create_response.json()["id"]
        
        # Now, update the created tutorial
        update_payload = {"title": "Updated Tutorial", "description": "Updated Description", "published": False}
        response = await ac.put(f"/tutorials/{tutorial_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Tutorial"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["published"] is False

@pytest.mark.asyncio
async def test_delete_tutorial():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First, create a tutorial to ensure there is one to delete
        payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
        create_response = await ac.post("/tutorials/", json=payload)
        tutorial_id = create_response.json()["id"]
        
        # Now, delete the created tutorial
        response = await ac.delete(f"/tutorials/{tutorial_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Tutorial deleted successfully"

@pytest.mark.asyncio
async def test_delete_all_tutorials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/tutorials/")
    assert response.status_code == 200
    assert response.json()["message"] == "All tutorials deleted successfully"
