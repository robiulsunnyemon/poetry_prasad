from pydantic import Field
from beanie import Document,Link
from prasad.auth.model.user import UserModel
from prasad.services.drone_services.model.drone_service import DroneServiceModel
import uuid
from datetime import datetime,timezone



class DroneServiceOrderModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    drone_services:Link[DroneServiceModel]
    service_date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    service_location:str
    order_status:str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "drone_service_order"