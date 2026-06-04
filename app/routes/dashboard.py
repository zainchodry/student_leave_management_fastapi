from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.leave import LeaveRequest
from app.models.attendance import Attendance

from app.utils.roles import (
    student_required,
    teacher_required,
    admin_required
)

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

@router.get("/student")
def student_dashboard(

    current_user=Depends(
        student_required
    ),

    db: Session = Depends(get_db)
):

    return {

        "total_leaves":

        db.query(
            LeaveRequest
        ).filter(
            LeaveRequest.student_id ==
            current_user.id
        ).count(),

        "attendance_records":

        db.query(
            Attendance
        ).filter(
            Attendance.student_id ==
            current_user.id
        ).count()
    }

@router.get("/teacher")
def teacher_dashboard(

    current_user=Depends(
        teacher_required
    ),

    db: Session = Depends(get_db)
):

    return {

        "pending_leaves":

        db.query(
            LeaveRequest
        ).filter(
            LeaveRequest.status ==
            "PENDING"
        ).count()
    }

@router.get("/admin")
def admin_dashboard(

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    return {

        "total_leaves":
        db.query(
            LeaveRequest
        ).count(),

        "total_attendance":
        db.query(
            Attendance
        ).count()
    }

