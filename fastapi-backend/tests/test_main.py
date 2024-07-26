import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_tutorial():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
        response = await ac.post("/tutorials/", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Tutorial"
    assert response_data["description"] == "Test Description"
    assert response_data["published"] is True
    assert "id" in response_data

@pytest.mark.asyncio
async def test_get_all_tutorials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tutorials/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for tutorial in response_data:
        assert "title" in tutorial
        assert "description" in tutorial
        assert "published" in tutorial

@pytest.mark.asyncio
async def test_get_all_published_tutorials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tutorials/published")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for tutorial in response_data:
        assert tutorial["published"] is True

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
    response_data = response.json()
    assert response_data["title"] == "Test Tutorial"
    assert response_data["description"] == "Test Description"
    assert response_data["published"] is True
    assert response_data["id"] == tutorial_id

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
    response_data = response.json()
    assert response_data["title"] == "Updated Tutorial"
    assert response_data["description"] == "Updated Description"
    assert response_data["published"] is False
    assert response_data["id"] == tutorial_id

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
    response_data = response.json()
    assert response_data["message"] == "Tutorial deleted successfully"

@pytest.mark.asyncio
async def test_delete_all_tutorials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/tutorials/")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "All tutorials deleted successfully"
