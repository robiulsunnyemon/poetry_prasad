from pydantic import Field
from beanie import Document,Link
from prasad.auth.model.user import UserModel
import uuid
from datetime import datetime,timezone



class DroneServiceModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    service_title: str
    service_price: str
    industry: str
    sub_industry: str
    service_description: str
    service_location:str


    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



    class Settings:
        name = "drone_service"