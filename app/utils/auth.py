from fastapi import Depends

from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database import get_db

from app.utils.security import decode_access_token

from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/accounts/login"
)

def get_current_user(

    token: str = Depends(
        oauth2_scheme
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        payload = decode_access_token(
            token
        )

        user_id = payload.get("user_id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )
    
