from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    marked_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    date = Column(
        Date
    )

    status = Column(
        String(50)
    )

    remarks = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )