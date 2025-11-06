from pydantic import Field
from beanie import Document,Link
from prasad.auth.model.user import UserModel
import uuid

class OperatorLicenseModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    license_number:str
    license_issue_date:str
    license_expiration_date:str
    additional_information:str



    model_config = {
        "collection": "license_history",
        "from_attributes": True
    }
