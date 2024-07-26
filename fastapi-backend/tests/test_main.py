import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.main import app  # Assuming the FastAPI app is instantiated in app/main.py
from app.models.tutorial import Tutorial, Base
from app.database import get_db

# Setup the database for testing
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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

def test_database_connection():
    # Test database connection
    try:
        db = TestingSessionLocal()
        db.execute("SELECT 1")
        assert True
    except Exception as e:
        assert False, f"Database connection failed: {e}"
    finally:
        db.close()

def test_database_insert_and_query(db: Session):
    # Test inserting and querying data in the database
    new_tutorial = Tutorial(title="DB Test Title", description="DB Test Description", published=True)
    db.add(new_tutorial)
    db.commit()
    db.refresh(new_tutorial)

    queried_tutorial = db.query(Tutorial).filter(Tutorial.title == "DB Test Title").first()
    assert queried_tutorial is not None
    assert queried_tutorial.title == "DB Test Title"
    assert queried_tutorial.description == "DB Test Description"
    assert queried_tutorial.published is True

def test_database_update(db: Session):
    # Test updating data in the database
    tutorial = db.query(Tutorial).filter(Tutorial.title == "DB Test Title").first()
    tutorial.title = "DB Updated Title"
    db.commit()
    db.refresh(tutorial)

    updated_tutorial = db.query(Tutorial).filter(Tutorial.title == "DB Updated Title").first()
    assert updated_tutorial is not None
    assert updated_tutorial.title == "DB Updated Title"

def test_database_delete(db: Session):
    # Test deleting data from the database
    tutorial = db.query(Tutorial).filter(Tutorial.title == "DB Updated Title").first()
    db.delete(tutorial)
    db.commit()

    deleted_tutorial = db.query(Tutorial).filter(Tutorial.title == "DB Updated Title").first()
    assert deleted_tutorial is None
