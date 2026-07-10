from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class PasswordReset(BaseModel):
    token: str
    new_password: str

class ForgotPassword(BaseModel):
    email: EmailStr
