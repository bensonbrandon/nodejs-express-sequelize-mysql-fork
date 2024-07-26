from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud
from app.database import get_db

router = APIRouter()

# Create and Save a new Tutorial
@router.post("/tutorials", response_model=schemas.Tutorial)
def create_tutorial(tutorial: schemas.TutorialCreate, db: Session = Depends(get_db)):
    if not tutorial.title:
        raise HTTPException(status_code=400, detail="Content can not be empty!")
    
    return crud.create_tutorial(db=db, tutorial=tutorial)

# Retrieve all Tutorials from the database.
@router.get("/tutorials", response_model=List[schemas.Tutorial])
def find_all_tutorials(title: str = None, db: Session = Depends(get_db)):
    if title:
        return crud.get_tutorials_by_title(db, title=title)
    return crud.get_tutorials(db)

# Find a single Tutorial with an id
@router.get("/tutorials/{id}", response_model=schemas.Tutorial)
def find_one_tutorial(id: int, db: Session = Depends(get_db)):
    db_tutorial = crud.get_tutorial(db, tutorial_id=id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail=f"Cannot find Tutorial with id={id}.")
    return db_tutorial

# Update a Tutorial by the id in the request
@router.put("/tutorials/{id}", response_model=schemas.Tutorial)
def update_tutorial(id: int, tutorial: schemas.TutorialUpdate, db: Session = Depends(get_db)):
    db_tutorial = crud.get_tutorial(db, tutorial_id=id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail=f"Cannot find Tutorial with id={id}.")
    
    return crud.update_tutorial(db=db, tutorial_id=id, tutorial=tutorial)

# Delete a Tutorial with the specified id in the request
@router.delete("/tutorials/{id}", response_model=schemas.Tutorial)
def delete_tutorial(id: int, db: Session = Depends(get_db)):
    db_tutorial = crud.get_tutorial(db, tutorial_id=id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail=f"Cannot find Tutorial with id={id}.")
    
    return crud.delete_tutorial(db=db, tutorial_id=id)

# Delete all Tutorials from the database.
@router.delete("/tutorials", response_model=schemas.Message)
def delete_all_tutorials(db: Session = Depends(get_db)):
    count = crud.delete_all_tutorials(db)
    return {"message": f"{count} Tutorials were deleted successfully!"}

# find all published Tutorial
@router.get("/tutorials/published", response_model=List[schemas.Tutorial])
def find_all_published_tutorials(db: Session = Depends(get_db)):
    return crud.get_published_tutorials(db)
