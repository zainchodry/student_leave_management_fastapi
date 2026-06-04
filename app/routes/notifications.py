from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.notification import Notification

from app.utils.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)

@router.get("/my")
def my_notifications(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return db.query(
        Notification
    ).filter(

        Notification.receiver_id
        ==
        current_user.id

    ).all()

@router.get("/unread-count")
def unread_count(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    count = db.query(
        Notification
    ).filter(

        Notification.receiver_id ==
        current_user.id,

        Notification.is_read == False

    ).count()

    return {
        "unread_notifications":
        count
    }

@router.put("/mark-read/{notification_id}")
def mark_read(

    notification_id: int,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    notification = db.query(
        Notification
    ).filter(

        Notification.id ==
        notification_id

    ).first()

    if notification:

        notification.is_read = True

        db.commit()

    return {
        "message":
        "Notification marked as read"
    }

