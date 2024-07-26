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
    response = client.post("/api/tutorials/", json={"title": "Test Title", "description": "Test Description", "published": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["published"] is True

def test_read_tutorials(db: Session):
    # Test reading all tutorials
    response = client.get("/api/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_published_tutorials(db: Session):
    # Test reading all published tutorials
    response = client.get("/api/tutorials/published")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(tutorial["published"] is True for tutorial in data)

def test_read_tutorial(db: Session):
    # Test reading a single tutorial by id
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Test Title").first()
    response = client.get(f"/api/tutorials/{tutorial.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["published"] is True

def test_update_tutorial(db: Session):
    # Test updating a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Test Title").first()
    response = client.put(f"/api/tutorials/{tutorial.id}", json={"title": "Updated Title", "description": "Updated Description", "published": False})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["published"] is False

def test_delete_tutorial(db: Session):
    # Test deleting a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Updated Title").first()
    response = client.delete(f"/api/tutorials/{tutorial.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["published"] is False

    # Verify the tutorial is deleted
    response = client.get(f"/api/tutorials/{tutorial.id}")
    assert response.status_code == 404

def test_delete_all_tutorials(db: Session):
    # Test deleting all tutorials
    response = client.delete("/api/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Verify all tutorials are deleted
    response = client.get("/api/tutorials/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_database_connection():
    # Test database connection
    try:
        db = TestingSessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        db.close()

def test_database_schema():
    # Test database schema
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "tutorial" in tables
    columns = [column['name'] for column in inspector.get_columns("tutorial")]
    assert "id" in columns
    assert "title" in columns
    assert "description" in columns
    assert "published" in columns
