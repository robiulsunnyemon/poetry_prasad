from pydantic import Field
from beanie import Document,Link
from prasad.auth.model.user import UserModel
import uuid




class IndustryModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    industry_title: str


    model_config = {
        "collection": "industry",
        "from_attributes": True
    }



class SubIndustryModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    sub_industry_title: str


    model_config = {
        "collection": "sub_industry",
        "from_attributes": True
    }