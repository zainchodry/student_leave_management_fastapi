from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.leave import LeaveRequest

from app.schemas.leave import (
    LeaveCreate,
    LeaveResponse,
    LeaveReviewSchema,
)

from app.schemas.statistics import (
    LeaveStatisticsResponse
)

from app.utils.roles import (
    student_required,
    teacher_required,
    admin_required
)

router = APIRouter(
    prefix="/api/leaves",
    tags=["Leaves"]
)

@router.post(
    "/apply",
    response_model=LeaveResponse
)
def apply_leave(

    payload: LeaveCreate,

    current_user=Depends(
        student_required
    ),

    db: Session = Depends(get_db)
):

    leave = LeaveRequest(

        student_id=current_user.id,

        leave_type=payload.leave_type,

        start_date=payload.start_date,

        end_date=payload.end_date,

        reason=payload.reason
    )

    db.add(leave)

    db.commit()

    db.refresh(leave)

    return leave

@router.get(
    "/my-leaves",
    response_model=list[LeaveResponse]
)
def my_leaves(

    current_user=Depends(
        student_required
    ),

    db: Session = Depends(get_db)
):

    return db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.student_id ==
        current_user.id

    ).all()

@router.put(
    "/cancel/{leave_id}"
)
def cancel_leave(

    leave_id: int,

    current_user=Depends(
        student_required
    ),

    db: Session = Depends(get_db)
):

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id == leave_id,

        LeaveRequest.student_id ==
        current_user.id

    ).first()

    if not leave:

        raise HTTPException(

            status_code=404,

            detail="Leave not found"
        )

    if leave.status != "PENDING":

        raise HTTPException(

            status_code=400,

            detail="Cannot cancel"
        )

    leave.status = "CANCELLED"

    db.commit()

    return {

        "message":
        "Leave cancelled successfully"
    }

@router.get(
    "/pending",
    response_model=list[LeaveResponse]
)
def pending_leaves(

    current_user=Depends(
        teacher_required
    ),

    db: Session = Depends(get_db)
):

    return db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.status == "PENDING"

    ).all()

@router.put(
    "/review/{leave_id}"
)
def review_leave(

    leave_id: int,

    payload: LeaveReviewSchema,

    current_user=Depends(
        teacher_required
    ),

    db: Session = Depends(get_db)
):

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id == leave_id

    ).first()

    if not leave:

        raise HTTPException(

            status_code=404,

            detail="Leave not found"
        )

    leave.status = payload.status

    leave.teacher_remark = (
        payload.teacher_remark
    )

    db.commit()

    return {

        "message":
        "Leave reviewed successfully"
    }

@router.get(
    "/all",
    response_model=list[LeaveResponse]
)
def all_leaves(

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    return db.query(
        LeaveRequest
    ).all()

@router.delete(
    "/delete/{leave_id}"
)
def delete_leave(

    leave_id: int,

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id == leave_id

    ).first()

    if not leave:

        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    db.delete(leave)

    db.commit()

    return {
        "message":
        "Leave deleted successfully"
    }

@router.get(
    "/statistics",
    response_model=LeaveStatisticsResponse
)
def leave_statistics(

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    total = db.query(
        LeaveRequest
    ).count()

    pending = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "PENDING"
    ).count()

    approved = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "APPROVED"
    ).count()

    rejected = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "REJECTED"
    ).count()

    cancelled = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "CANCELLED"
    ).count()

    return {

        "total_leaves": total,

        "pending": pending,

        "approved": approved,

        "rejected": rejected,

        "cancelled": cancelled
    }