from pydantic import BaseModel

class IndustryResponse(BaseModel):
    industry_title: str


class SubIndustryResponse(BaseModel):
    sub_industry_title: str