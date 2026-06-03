from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class LeaveRequest(Base):

    __tablename__ = "leave_requests"

    id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    leave_type = Column(
        String(50)
    )

    start_date = Column(
        Date
    )

    end_date = Column(
        Date
    )

    reason = Column(
        Text
    )

    teacher_remark = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        default="PENDING"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    