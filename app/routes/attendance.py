from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.attendance import Attendance

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendancePercentageResponse
)

from app.utils.roles import (
    student_required,
    teacher_required,
    admin_required
)

router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"]
)

@router.post(
    "/mark",
    response_model=AttendanceResponse
)
def mark_attendance(

    payload: AttendanceCreate,

    current_user=Depends(
        teacher_required
    ),

    db: Session = Depends(get_db)
):

    attendance = Attendance(

        student_id=payload.student_id,

        date=payload.date,

        status=payload.status,

        remarks=payload.remarks,

        marked_by=current_user.id
    )

    db.add(attendance)

    db.commit()

    db.refresh(attendance)

    return attendance

@router.put(
    "/update/{attendance_id}"
)
def update_attendance(

    attendance_id: int,

    payload: AttendanceUpdate,

    current_user=Depends(
        teacher_required
    ),

    db: Session = Depends(get_db)
):

    attendance = db.query(
        Attendance
    ).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:

        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    attendance.status = payload.status
    attendance.remarks = payload.remarks

    db.commit()

    return {
        "message":
        "Attendance updated"
    }

@router.get(
    "/my",
    response_model=list[AttendanceResponse]
)
def my_attendance(

    current_user=Depends(
        student_required
    ),

    db: Session = Depends(get_db)
):

    return db.query(
        Attendance
    ).filter(
        Attendance.student_id ==
        current_user.id
    ).all()

@router.get(
    "/percentage",
    response_model=AttendancePercentageResponse
)
def attendance_percentage(

    current_user=Depends(
        student_required
    ),

    db: Session = Depends(get_db)
):

    total = db.query(
        Attendance
    ).filter(
        Attendance.student_id ==
        current_user.id
    ).count()

    present = db.query(
        Attendance
    ).filter(
        Attendance.student_id ==
        current_user.id,

        Attendance.status ==
        "PRESENT"
    ).count()

    percentage = 0

    if total > 0:

        percentage = round(
            (present / total) * 100,
            2
        )

    return {

        "total_days": total,

        "present_days": present,

        "attendance_percentage":
        percentage
    }

@router.get(
    "/statistics"
)
def attendance_statistics(

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    return {

        "total_records":
        db.query(
            Attendance
        ).count(),

        "present":
        db.query(
            Attendance
        ).filter(
            Attendance.status ==
            "PRESENT"
        ).count(),

        "absent":
        db.query(
            Attendance
        ).filter(
            Attendance.status ==
            "ABSENT"
        ).count(),

        "leave":
        db.query(
            Attendance
        ).filter(
            Attendance.status ==
            "LEAVE"
        ).count()
    }