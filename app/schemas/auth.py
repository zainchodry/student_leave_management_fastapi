from pydantic import (
    BaseModel,
    EmailStr
)

class LoginSchema(BaseModel):

    email: EmailStr

    password: str

class TokenResponse(BaseModel):

    access_token: str

    token_type: str

    role: str

class ChangePasswordSchema(BaseModel):

    old_password: str

    new_password: str

class ForgotPasswordSchema(BaseModel):

    email: EmailStr

class ResetPasswordSchema(BaseModel):

    email: EmailStr

    otp: str

    new_password: str