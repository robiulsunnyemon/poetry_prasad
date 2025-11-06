from pydantic import BaseModel



class EquipmentBase(BaseModel):
    equipment_id:str
    asset_id:str
    equipment_type:str
    model:str
    make:str
    manufacturer:str
    year:str
    serial_number:str
    last_maintenance_date:str



class EquipmentCreate(EquipmentBase):
    pass


class EquipmentResponse(EquipmentBase):
    pass