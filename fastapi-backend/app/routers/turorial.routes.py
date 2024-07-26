from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import tutorial_model
from app.schemas import tutorial_schema
from app.database import get_db

router = APIRouter(
    prefix="/api/tutorials",
    tags=["tutorials"],
    responses={404: {"description": "Not found"}},
)

# Create a new Tutorial
@router.post("/", response_model=tutorial_schema.Tutorial)
def create_tutorial(tutorial: tutorial_schema.TutorialCreate, db: Session = Depends(get_db)):
    db_tutorial = tutorial_model.Tutorial(**tutorial.dict())
    db.add(db_tutorial)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

# Retrieve all Tutorials
@router.get("/", response_model=List[tutorial_schema.Tutorial])
def read_tutorials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tutorials = db.query(tutorial_model.Tutorial).offset(skip).limit(limit).all()
    return tutorials

# Retrieve all published Tutorials
@router.get("/published", response_model=List[tutorial_schema.Tutorial])
def read_published_tutorials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tutorials = db.query(tutorial_model.Tutorial).filter(tutorial_model.Tutorial.published == True).offset(skip).limit(limit).all()
    return tutorials

# Retrieve a single Tutorial with id
@router.get("/{id}", response_model=tutorial_schema.Tutorial)
def read_tutorial(id: int, db: Session = Depends(get_db)):
    tutorial = db.query(tutorial_model.Tutorial).filter(tutorial_model.Tutorial.id == id).first()
    if tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial

# Update a Tutorial with id
@router.put("/{id}", response_model=tutorial_schema.Tutorial)
def update_tutorial(id: int, tutorial: tutorial_schema.TutorialUpdate, db: Session = Depends(get_db)):
    db_tutorial = db.query(tutorial_model.Tutorial).filter(tutorial_model.Tutorial.id == id).first()
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    for key, value in tutorial.dict().items():
        setattr(db_tutorial, key, value)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

# Delete a Tutorial with id
@router.delete("/{id}", response_model=tutorial_schema.Tutorial)
def delete_tutorial(id: int, db: Session = Depends(get_db)):
    db_tutorial = db.query(tutorial_model.Tutorial).filter(tutorial_model.Tutorial.id == id).first()
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    db.delete(db_tutorial)
    db.commit()
    return db_tutorial

# Delete all Tutorials
@router.delete("/", response_model=List[tutorial_schema.Tutorial])
def delete_all_tutorials(db: Session = Depends(get_db)):
    tutorials = db.query(tutorial_model.Tutorial).all()
    for tutorial in tutorials:
        db.delete(tutorial)
    db.commit()
    return tutorials
