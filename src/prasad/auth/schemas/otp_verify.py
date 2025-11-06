from pydantic import BaseModel


class UserOTPVerify(BaseModel):
    email: str
    otp: str