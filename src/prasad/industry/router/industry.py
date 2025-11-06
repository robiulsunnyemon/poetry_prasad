from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.utils.user_info import get_user_info
from prasad.industry.model.industry import IndustryModel,SubIndustryModel
from typing import List
from prasad.industry.schemas.industry import IndustryResponse,SubIndustryResponse

router = APIRouter(tags=["Industry & Sub Industry"])


@router.post("/industry", status_code=status.HTTP_201_CREATED)
async def create_industry(industry_title:str,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not admin")

    new_industry = IndustryModel(
        user_id=db_user,
        industry_title=industry_title,
    )

    await new_industry.insert()
    return {"message": "success"}




@router.get("/industry",response_model=List[IndustryResponse] ,status_code=status.HTTP_200_OK)
async def read_industry():
    return await IndustryModel.find().to_list()



@router.post("/sub_industry", status_code=status.HTTP_201_CREATED)
async def create_industry(sub_industry_title:str,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not admin")

    new_sub_industry = SubIndustryModel(
        user_id=db_user,
        sub_industry_title=sub_industry_title,
    )

    await new_sub_industry.insert()
    return {"message": "success"}


@router.get("/sub_industry",response_model=List[SubIndustryResponse] ,status_code=status.HTTP_200_OK)
async def read_sub_industry():
    return await SubIndustryModel.find().to_list()
