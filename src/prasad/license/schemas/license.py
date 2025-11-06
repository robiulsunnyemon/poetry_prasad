from pydantic import BaseModel

class LicenseBase(BaseModel):
    license_number:str
    license_issue_date:str
    license_expiration_date:str
    additional_information:str

class LicenseCreate(LicenseBase):
    pass

class LicenseResponse(LicenseBase):
    pass