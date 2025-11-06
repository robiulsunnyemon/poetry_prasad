from  pydantic import Field
from beanie import Document,Link
import uuid
from datetime import datetime,timezone
from prasad.auth.model.user import UserModel


class CustomerInfoModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    first_name:str
    middle_name:str
    last_name:str
    nickname:str
    phone:str
    district:str
    mondal:str
    village:str
    registered_by:str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "collection": "customer_info",
        "from_attributes": True
    }



class CustomerDetailsInfoModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    kyc_number: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    industry: str
    sub_industry: str

    model_config = {
        "collection": "customer_details_info",
        "from_attributes": True
    }


class CustomerServicesDetailsModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    location_name: str
    latitude_longitude: str
    land_size: str
    unit: str
    instructions: str

    model_config = {
        "collection": "customer_services_info",
        "from_attributes": True
    }