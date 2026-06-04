from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.utils.auth import (
    get_current_user
)

from app.models.user import User
from app.models.profile import Profile
from app.models.password_reset import PasswordResetOTP

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.schemas.profile import (
    ProfileUpdate,
    ProfileResponse
)

from app.schemas.auth import (
    LoginSchema,
    TokenResponse,
    ChangePasswordSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)

from app.utils.otp import generate_otp
from app.utils.email import send_otp_email


router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"]
)

@router.post(
    "/register",
    response_model=UserResponse
)
def register(

    payload: UserCreate,

    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = User(

        username=payload.username,

        email=payload.email,

        password=hash_password(
            payload.password
        ),

        role=payload.role
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    profile = Profile(
        user_id=user.id
    )

    db.add(profile)

    db.commit()

    return user

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(

    payload: LoginSchema,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not verify_password(
        payload.password,
        user.password
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    token = create_access_token({

        "user_id": user.id,

        "role": user.role
    })

    return {

        "access_token": token,

        "token_type": "bearer",

        "role": user.role
    }

@router.get(
    "/profile",
    response_model=ProfileResponse
)
def get_profile(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    profile = db.query(Profile).filter(

        Profile.user_id == current_user.id

    ).first()

    return profile

@router.put(
    "/profile",
    response_model=ProfileResponse
)
def update_profile(

    payload: ProfileUpdate,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    profile = db.query(Profile).filter(

        Profile.user_id == current_user.id

    ).first()

    for key, value in payload.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            profile,
            key,
            value
        )

    db.commit()

    db.refresh(profile)

    return profile

@router.post(
    "/change-password"
)
def change_password(

    payload: ChangePasswordSchema,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    if not verify_password(

        payload.old_password,

        current_user.password

    ):

        raise HTTPException(

            status_code=400,

            detail="Old password incorrect"
        )

    current_user.password = hash_password(
        payload.new_password
    )

    db.commit()

    return {

        "message":
        "Password changed successfully"
    }

@router.post(
    "/forgot-password"
)
def forgot_password(

    payload: ForgotPasswordSchema,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(

        User.email == payload.email

    ).first()

    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )

    otp = generate_otp()

    otp_obj = PasswordResetOTP(

        user_id=user.id,

        otp=otp
    )

    db.add(otp_obj)

    db.commit()

    send_otp_email(
        user.email,
        otp
    )

    return {

        "message":
        "OTP sent successfully"
    }

@router.post(
    "/reset-password"
)
def reset_password(

    payload: ResetPasswordSchema,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(

        User.email == payload.email

    ).first()

    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )

    otp_record = db.query(
        PasswordResetOTP
    ).filter(

        PasswordResetOTP.user_id == user.id,

        PasswordResetOTP.otp == payload.otp

    ).first()

    if not otp_record:

        raise HTTPException(

            status_code=400,

            detail="Invalid OTP"
        )

    user.password = hash_password(
        payload.new_password
    )

    db.commit()

    return {

        "message":
        "Password reset successfully"
    }
