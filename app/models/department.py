from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from app.database import Base


class Department(Base):

    __tablename__ = "departments"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(255),
        unique=True
    )

    description = Column(
        Text,
        nullable=True
    )

    head_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
