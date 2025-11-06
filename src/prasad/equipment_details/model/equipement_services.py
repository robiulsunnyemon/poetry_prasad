from pydantic import Field
from beanie import Document,Link
from prasad.auth.model.user import UserModel
import uuid
from datetime import datetime,timezone


class EquipmentHistoryModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    equipment_id:str
    asset_id:str
    equipment_type:str
    model:str
    make:str
    manufacturer:str
    year:str
    serial_number:str
    last_maintenance_date:str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    model_config = {
        "collection": "equipment_history",
        "from_attributes": True
    }