from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    
class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"