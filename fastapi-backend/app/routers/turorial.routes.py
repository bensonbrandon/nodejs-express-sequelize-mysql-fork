from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

# Assuming the controller functions are defined in a separate module
from ..controllers import tutorial_controller

router = APIRouter()

class Tutorial(BaseModel):
    title: str
    description: str
    published: bool

# Create a new Tutorial
@router.post("/", response_model=Tutorial)
async def create_tutorial(tutorial: Tutorial):
    return await tutorial_controller.create(tutorial)

# Retrieve all Tutorials
@router.get("/", response_model=List[Tutorial])
async def get_all_tutorials():
    return await tutorial_controller.find_all()

# Retrieve all published Tutorials
@router.get("/published", response_model=List[Tutorial])
async def get_all_published_tutorials():
    return await tutorial_controller.find_all_published()

# Retrieve a single Tutorial with id
@router.get("/{id}", response_model=Tutorial)
async def get_tutorial(id: int):
    tutorial = await tutorial_controller.find_one(id)
    if tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial

# Update a Tutorial with id
@router.put("/{id}", response_model=Tutorial)
async def update_tutorial(id: int, tutorial: Tutorial):
    updated_tutorial = await tutorial_controller.update(id, tutorial)
    if updated_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return updated_tutorial

# Delete a Tutorial with id
@router.delete("/{id}")
async def delete_tutorial(id: int):
    result = await tutorial_controller.delete(id)
    if not result:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return {"message": "Tutorial deleted successfully"}

# Delete all Tutorials
@router.delete("/")
async def delete_all_tutorials():
    await tutorial_controller.delete_all()
    return {"message": "All tutorials deleted successfully"}
