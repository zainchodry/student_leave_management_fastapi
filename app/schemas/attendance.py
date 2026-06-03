from pydantic import BaseModel
from datetime import date
from typing import Optional

class AttendanceCreate(BaseModel):

    student_id: int

    date: date

    status: str

    remarks: Optional[str] = None

class AttendanceUpdate(BaseModel):

    status: str

    remarks: Optional[str] = None

class AttendanceResponse(BaseModel):

    id: int

    student_id: int

    marked_by: int

    date: date

    status: str

    remarks: Optional[str]

    class Config:

        from_attributes = True

class AttendancePercentageResponse(BaseModel):

    total_days: int

    present_days: int

    attendance_percentage: float

