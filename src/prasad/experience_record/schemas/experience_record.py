from pydantic import BaseModel


class OperatorRecordBase(BaseModel):
    total_flight_hours:str
    past_project_and_events:str


class OperatorRecordCreate(OperatorRecordBase):
    pass

class OperatorRecordResponse(OperatorRecordBase):
    pass
