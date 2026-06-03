from pydantic import BaseModel
from typing import Optional


class ProfileUpdate(BaseModel):

    phone_number: Optional[str] = None

    address: Optional[str] = None

    department: Optional[str] = None

    profile_picture: Optional[str] = None


class ProfileResponse(BaseModel):

    id: int

    user_id: int

    phone_number: str | None

    address: str | None

    department: str | None

    profile_picture: str | None

    class Config:

        from_attributes = True