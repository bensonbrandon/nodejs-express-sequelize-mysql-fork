import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.main import app  # Assuming your FastAPI app is instantiated in app/main.py
from app.models.tutorial import Tutorial, Base
from app.schemas import TutorialCreate, TutorialUpdate

# Setup the database for testing
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    # Create a new database session for a test
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_tutorial(client: TestClient, db: Session):
    # Test creating a new tutorial
    tutorial_data = {"title": "Test Title", "description": "Test Description", "published": True}
    response = client.post("/tutorials/", json=tutorial_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["published"] is True

def test_get_all_tutorials(client: TestClient, db: Session):
    # Test retrieving all tutorials
    response = client.get("/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_all_published_tutorials(client: TestClient, db: Session):
    # Test retrieving all published tutorials
    response = client.get("/tutorials/published")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(tutorial["published"] for tutorial in data)

def test_get_tutorial(client: TestClient, db: Session):
    # Test retrieving a single tutorial by id
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Test Title").first()
    response = client.get(f"/tutorials/{tutorial.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["published"] is True

def test_update_tutorial(client: TestClient, db: Session):
    # Test updating a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Test Title").first()
    update_data = {"title": "Updated Title", "description": "Updated Description", "published": False}
    response = client.put(f"/tutorials/{tutorial.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["published"] is False

def test_delete_tutorial(client: TestClient, db: Session):
    # Test deleting a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Updated Title").first()
    response = client.delete(f"/tutorials/{tutorial.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["published"] is False

    # Verify the tutorial is deleted
    response = client.get(f"/tutorials/{tutorial.id}")
    assert response.status_code == 404

def test_delete_all_tutorials(client: TestClient, db: Session):
    # Test deleting all tutorials
    response = client.delete("/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Verify all tutorials are deleted
    response = client.get("/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
