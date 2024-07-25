from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

# Example route definitions
@router.get("/tutorials", response_model=List[str])
async def get_tutorials():
    """
    Get a list of all tutorials.
    """
    # Placeholder for actual implementation
    return ["Tutorial 1", "Tutorial 2"]

@router.get("/tutorials/{tutorial_id}", response_model=str)
async def get_tutorial(tutorial_id: int):
    """
    Get a specific tutorial by ID.
    """
    # Placeholder for actual implementation
    if tutorial_id == 1:
        return "Tutorial 1"
    else:
        raise HTTPException(status_code=404, detail="Tutorial not found")

@router.post("/tutorials", response_model=str)
async def create_tutorial(tutorial: str):
    """
    Create a new tutorial.
    """
    # Placeholder for actual implementation
    return f"Created tutorial: {tutorial}"

@router.put("/tutorials/{tutorial_id}", response_model=str)
async def update_tutorial(tutorial_id: int, tutorial: str):
    """
    Update an existing tutorial by ID.
    """
    # Placeholder for actual implementation
    if tutorial_id == 1:
        return f"Updated tutorial {tutorial_id} to {tutorial}"
    else:
        raise HTTPException(status_code=404, detail="Tutorial not found")

@router.delete("/tutorials/{tutorial_id}", response_model=str)
async def delete_tutorial(tutorial_id: int):
    """
    Delete a tutorial by ID.
    """
    # Placeholder for actual implementation
    if tutorial_id == 1:
        return f"Deleted tutorial {tutorial_id}"
    else:
        raise HTTPException(status_code=404, detail="Tutorial not found")
