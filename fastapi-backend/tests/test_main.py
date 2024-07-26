import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.models.tutorial import Tutorial, Base

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

def test_create_tutorial(db: Session):
    # Test creating a new tutorial
    new_tutorial = Tutorial(title="Test Title", description="Test Description", published=True)
    db.add(new_tutorial)
    db.commit()
    db.refresh(new_tutorial)
    
    assert new_tutorial.id is not None
    assert new_tutorial.title == "Test Title"
    assert new_tutorial.description == "Test Description"
    assert new_tutorial.published is True

def test_read_tutorial(db: Session):
    # Test reading a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Test Title").first()
    
    assert tutorial is not None
    assert tutorial.title == "Test Title"
    assert tutorial.description == "Test Description"
    assert tutorial.published is True

def test_update_tutorial(db: Session):
    # Test updating a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Test Title").first()
    tutorial.title = "Updated Title"
    db.commit()
    db.refresh(tutorial)
    
    assert tutorial.title == "Updated Title"

def test_delete_tutorial(db: Session):
    # Test deleting a tutorial
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Updated Title").first()
    db.delete(tutorial)
    db.commit()
    
    tutorial = db.query(Tutorial).filter(Tutorial.title == "Updated Title").first()
    assert tutorial is None
