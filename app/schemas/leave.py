from pydantic import BaseModel
from datetime import date
from typing import Optional

class LeaveCreate(BaseModel):

    leave_type: str

    start_date: date

    end_date: date

    reason: str

class LeaveResponse(BaseModel):

    id: int

    student_id: int

    leave_type: str

    start_date: date

    end_date: date

    reason: str

    teacher_remark: Optional[str]

    status: str

    class Config:

        from_attributes = True

class LeaveReviewSchema(BaseModel):

    status: str

    teacher_remark: str

