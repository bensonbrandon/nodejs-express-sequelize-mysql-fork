from pydantic import BaseModel
from typing import Optional

class Tutorial(BaseModel):
    title: Optional[str]
    description: Optional[str]
    published: Optional[bool]

    class Config:
        orm_mode = True
