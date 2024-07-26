import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app  # Assuming the FastAPI app is instantiated in app/main.py
from app.models.tutorial import Tutorial, Base
from app.database import get_db

# Setup the database for testing
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    # Create a new database session for a test
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create_tutorial(db: Session):
    # Test creating a new tutorial
    response = client.post("/tutorials/", json={"title": "Test Title", "description": "Test Description", "published": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["published"] is True

def test_read_tutorials(db: Session):
    # Test reading all tutorials
    response = client.get("/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_published_tutorials(db: Session):
    # Test reading all published tutorials
    response = client.get("/tutorials/published")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(tutorial["published"] is True for tutorial in data)

def test_read_tutorial(db: Session):
    # Test reading a single tutorial
    response = client.get("/tutorials/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["published"] is True

def test_update_tutorial(db: Session):
    # Test updating a tutorial
    response = client.put("/tutorials/1", json={"title": "Updated Title", "description": "Updated Description", "published": False})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["published"] is False

def test_delete_tutorial(db: Session):
    # Test deleting a tutorial
    response = client.delete("/tutorials/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"

def test_delete_all_tutorials(db: Session):
    # Test deleting all tutorials
    response = client.delete("/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
