from pydantic import BaseModel,ConfigDict
from datetime import datetime

class CustomerInfoBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    nickname: str
    phone: str
    district: str
    mondal: str
    village: str
    registered_by: str

class CustomerInfoCreate(CustomerInfoBase):
    pass

class CustomerInfoResponse(CustomerInfoBase):
    pass

    class Config:ConfigDict(from_attributes=True)



class CustomerInfoDetailsBase(BaseModel):
    kyc_number: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    industry: str
    sub_industry: str

class CustomerInfoDetailsCreate(CustomerInfoDetailsBase):
    pass

class CustomerInfoDetailsResponse(CustomerInfoDetailsBase):
    pass



class CustomerServicesDetailsBase(BaseModel):
    location_name: str
    latitude_longitude: str
    land_size: str
    unit: str
    instructions: str


class CustomerServicesDetailsCreate(CustomerServicesDetailsBase):
    pass


class CustomerServicesDetailsResponse(CustomerServicesDetailsBase):
    pass