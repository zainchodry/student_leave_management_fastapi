from pydantic import BaseModel
from typing import Optional

class DepartmentCreate(BaseModel):

    name: str

    description: Optional[str] = None

    head_id: Optional[int] = None

class DepartmentUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    head_id: Optional[int] = None

class DepartmentResponse(BaseModel):

    id: int

    name: str

    description: Optional[str]

    head_id: Optional[int]

    class Config:

        from_attributes = True

