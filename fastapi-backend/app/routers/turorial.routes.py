from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..controllers import tutorial_controller
from ..schemas import TutorialCreate, TutorialUpdate, Tutorial

router = APIRouter()

# Dependency to get the database session
def get_db():
    from ..database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new Tutorial
@router.post("/", response_model=Tutorial)
def create_tutorial(tutorial: TutorialCreate, db: Session = Depends(get_db)):
    return tutorial_controller.create(db=db, tutorial=tutorial)

# Retrieve all Tutorials
@router.get("/", response_model=List[Tutorial])
def read_tutorials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tutorials = tutorial_controller.get_all(db, skip=skip, limit=limit)
    return tutorials

# Retrieve all published Tutorials
@router.get("/published", response_model=List[Tutorial])
def read_published_tutorials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tutorials = tutorial_controller.get_all_published(db, skip=skip, limit=limit)
    return tutorials

# Retrieve a single Tutorial with id
@router.get("/{id}", response_model=Tutorial)
def read_tutorial(id: int, db: Session = Depends(get_db)):
    db_tutorial = tutorial_controller.get(db, tutorial_id=id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return db_tutorial

# Update a Tutorial with id
@router.put("/{id}", response_model=Tutorial)
def update_tutorial(id: int, tutorial: TutorialUpdate, db: Session = Depends(get_db)):
    db_tutorial = tutorial_controller.get(db, tutorial_id=id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial_controller.update(db=db, tutorial=tutorial, tutorial_id=id)

# Delete a Tutorial with id
@router.delete("/{id}", response_model=Tutorial)
def delete_tutorial(id: int, db: Session = Depends(get_db)):
    db_tutorial = tutorial_controller.get(db, tutorial_id=id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial_controller.delete(db=db, tutorial_id=id)

# Delete all Tutorials
@router.delete("/", response_model=List[Tutorial])
def delete_all_tutorials(db: Session = Depends(get_db)):
    return tutorial_controller.delete_all(db=db)
