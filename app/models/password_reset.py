from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class PasswordResetOTP(Base):

    __tablename__ = "password_reset_otps"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    otp = Column(
        String(6)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    