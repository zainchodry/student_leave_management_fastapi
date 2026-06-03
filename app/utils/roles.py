from fastapi import Depends

from fastapi import HTTPException

from app.utils.auth import (
    get_current_user
)

def student_required(
    current_user=Depends(
        get_current_user
    )
):

    if current_user.role != "STUDENT":

        raise HTTPException(
            status_code=403,
            detail="Student access only"
        )

    return current_user

def teacher_required(
    current_user=Depends(
        get_current_user
    )
):

    if current_user.role != "TEACHER":

        raise HTTPException(
            status_code=403,
            detail="Teacher access only"
        )

    return current_user

def admin_required(
    current_user=Depends(
        get_current_user
    )
):

    if current_user.role != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access only"
        )

    return current_user

