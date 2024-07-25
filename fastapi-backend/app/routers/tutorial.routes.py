from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Define a Pydantic model for the tutorial
class Tutorial(BaseModel):
    id: int
    title: str
    description: str

# In-memory storage for tutorials
tutorials = []

@router.get("/tutorials", response_model=List[Tutorial])
async def get_tutorials():
    return tutorials

@router.get("/tutorials/{tutorial_id}", response_model=Tutorial)
async def get_tutorial(tutorial_id: int):
    for tutorial in tutorials:
        if tutorial.id == tutorial_id:
            return tutorial
    raise HTTPException(status_code=404, detail="Tutorial not found")

@router.post("/tutorials", response_model=Tutorial)
async def create_tutorial(tutorial: Tutorial):
    tutorials.append(tutorial)
    return tutorial

@router.put("/tutorials/{tutorial_id}", response_model=Tutorial)
async def update_tutorial(tutorial_id: int, updated_tutorial: Tutorial):
    for index, tutorial in enumerate(tutorials):
        if tutorial.id == tutorial_id:
            tutorials[index] = updated_tutorial
            return updated_tutorial
    raise HTTPException(status_code=404, detail="Tutorial not found")

@router.delete("/tutorials/{tutorial_id}", response_model=Tutorial)
async def delete_tutorial(tutorial_id: int):
    for index, tutorial in enumerate(tutorials):
        if tutorial.id == tutorial_id:
            deleted_tutorial = tutorials.pop(index)
            return deleted_tutorial
    raise HTTPException(status_code=404, detail="Tutorial not found")
