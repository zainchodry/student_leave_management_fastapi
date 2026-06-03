from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


class Profile(Base):

    __tablename__ = "profiles"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    phone_number = Column(
        String(20),
        nullable=True
    )

    address = Column(
        String(500),
        nullable=True
    )

    department = Column(
        String(255),
        nullable=True
    )

    profile_picture = Column(
        String(500),
        nullable=True
    )

    user = relationship(
        "User"
    )
    