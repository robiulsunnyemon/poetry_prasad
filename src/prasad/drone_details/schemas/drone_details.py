from pydantic import BaseModel,ConfigDict


class DroneDetailsBase(BaseModel):
    drone_uin_uk: str
    services_capabilities: str
    model: str
    make: str
    serial_number: str
    manufacturer_year: str
    manufacturer: str
    flight_hours: str
    last_maintenance_date: str
    insurance_status: str
    rent_status: str
    operational_status: str
    battery_type: str
    battery_cycles: str
    battery_capacity: str
    drone_condition: str

    class Config: ConfigDict(from_attributes=True)

class DroneDetailsCreate(DroneDetailsBase):
    pass

class DroneDetailsResponse(DroneDetailsBase):
    id:str