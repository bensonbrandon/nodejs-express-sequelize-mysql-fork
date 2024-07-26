import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
from main import app

# Create a new database session for testing
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing session
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = _get_test_db
    with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_tutorial(client):
    payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
    response = await client.post("/tutorials/", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Tutorial"
    assert response_data["description"] == "Test Description"
    assert response_data["published"] is True
    assert "id" in response_data

@pytest.mark.asyncio
async def test_get_all_tutorials(client):
    response = await client.get("/tutorials/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for tutorial in response_data:
        assert "title" in tutorial
        assert "description" in tutorial
        assert "published" in tutorial

@pytest.mark.asyncio
async def test_get_all_published_tutorials(client):
    response = await client.get("/tutorials/published")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for tutorial in response_data:
        assert tutorial["published"] is True

@pytest.mark.asyncio
async def test_get_tutorial(client):
    # First, create a tutorial to ensure there is one to fetch
    payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
    create_response = await client.post("/tutorials/", json=payload)
    tutorial_id = create_response.json()["id"]
    
    # Now, fetch the created tutorial
    response = await client.get(f"/tutorials/{tutorial_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Test Tutorial"
    assert response_data["description"] == "Test Description"
    assert response_data["published"] is True
    assert response_data["id"] == tutorial_id

@pytest.mark.asyncio
async def test_update_tutorial(client):
    # First, create a tutorial to ensure there is one to update
    payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
    create_response = await client.post("/tutorials/", json=payload)
    tutorial_id = create_response.json()["id"]
    
    # Now, update the created tutorial
    update_payload = {"title": "Updated Tutorial", "description": "Updated Description", "published": False}
    response = await client.put(f"/tutorials/{tutorial_id}", json=update_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Updated Tutorial"
    assert response_data["description"] == "Updated Description"
    assert response_data["published"] is False
    assert response_data["id"] == tutorial_id

@pytest.mark.asyncio
async def test_delete_tutorial(client):
    # First, create a tutorial to ensure there is one to delete
    payload = {"title": "Test Tutorial", "description": "Test Description", "published": True}
    create_response = await client.post("/tutorials/", json=payload)
    tutorial_id = create_response.json()["id"]
    
    # Now, delete the created tutorial
    response = await client.delete(f"/tutorials/{tutorial_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Tutorial deleted successfully"

@pytest.mark.asyncio
async def test_delete_all_tutorials(client):
    response = await client.delete("/tutorials/")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "All tutorials deleted successfully"
