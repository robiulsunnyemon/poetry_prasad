from pydantic import  Field
import  uuid
from beanie import Document,Link
from prasad.auth.model.user import UserModel


class DroneDetailsModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id:Link[UserModel]
    drone_uin_uk: str
    services_capabilities: str
    model: str
    make: str
    manufacturer_year: str
    serial_number: str
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


    model_config = {
        "collection": "drone_details",
        "from_attributes": True
    }