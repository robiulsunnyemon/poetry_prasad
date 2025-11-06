from beanie import Document
from pydantic import EmailStr, Field
import uuid
from datetime import datetime, timezone

class UserModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    email: EmailStr
    password: str
    account_status: str
    role: str
    otp_status: str
    otp: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    model_config = {
        "collection": "user",
        "from_attributes": True
    }
