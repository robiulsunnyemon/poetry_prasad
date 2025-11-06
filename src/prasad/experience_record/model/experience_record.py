from pydantic import Field
from beanie import Document,Link
from prasad.auth.model.user import UserModel
import uuid

class OperatorRecordModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    total_flight_hours:str
    past_project_and_events:str


    model_config = {
        "collection": "experience_record",
        "from_attributes": True
    }