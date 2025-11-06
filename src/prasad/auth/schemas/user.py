from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    id:str
    email: EmailStr
    account_status: str
    role: str
    otp_status: str
    created_at: datetime


    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
