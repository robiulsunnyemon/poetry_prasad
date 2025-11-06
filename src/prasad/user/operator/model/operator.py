from pydantic import Field
from beanie import Document,Link
import uuid
from prasad.auth.model.user import UserModel


class OperatorInfoModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    first_name: str
    last_name: str
    phone_number: str
    latitude_longitude: str
    service_radius: str
    industry: str
    sub_industry: str

    model_config = {
        "collection": "operator_info",
        "from_attributes": True
    }