from typing import Optional

from pydantic import BaseModel
from datetime import datetime



class DroneServicesOrderCreate(BaseModel):
    drone_services_id: str
    service_date_time: datetime
    service_location:str



class DroneServicesOrderResponse(DroneServicesOrderCreate):
    order_status: str
    id: str
