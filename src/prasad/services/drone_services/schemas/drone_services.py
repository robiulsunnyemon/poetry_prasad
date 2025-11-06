from pydantic import BaseModel
from typing import Optional

class DroneServicesBase(BaseModel):
    service_title: str
    service_price: str
    industry: str
    sub_industry: str
    service_description: str
    service_location: str


class DroneServicesCreate(DroneServicesBase):
    pass

class DroneServicesResponse(DroneServicesBase):
    id: str

class DroneServicesUpdate(BaseModel):
    service_title: Optional[str] = None
    service_price: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    service_description: Optional[str] = None
    service_location: Optional[str] = None