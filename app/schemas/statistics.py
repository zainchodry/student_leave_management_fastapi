from pydantic import BaseModel

class LeaveStatisticsResponse(BaseModel):

    total_leaves: int

    pending: int

    approved: int

    rejected: int

    cancelled: int

class AttendanceStatisticsResponse(BaseModel):

    total_records: int

    present: int

    absent: int

    leave: int

