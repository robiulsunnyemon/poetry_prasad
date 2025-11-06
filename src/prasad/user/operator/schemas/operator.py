from pydantic import BaseModel,ConfigDict

class OperatorInfoBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    latitude_longitude: str
    service_radius: str
    industry: str
    sub_industry: str

    class Config:ConfigDict(from_attributes=True)

class OperatorInfoCreate(OperatorInfoBase):
    pass


class OperatorInfoResponse(OperatorInfoBase):
    pass
