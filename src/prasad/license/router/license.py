from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.utils.user_info import get_user_info
from prasad.license.model.license import OperatorLicenseModel
from prasad.license.schemas.license import LicenseCreate


router = APIRouter(prefix="/license", tags=["License and Certificates"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_license(license_data: LicenseCreate,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not db_user.role=="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not operator")

    new_license=OperatorLicenseModel(
        user_id=db_user,
        license_number=license_data.license_number,
        license_issue_date=license_data.license_issue_date,
        license_expiration_date=license_data.license_expiration_date,
        additional_information=license_data.additional_information,
    )
    await new_license.insert()
    return new_license



# @router.get("/",status_code=status.HTTP_200_OK)
# async def get_all_licenses():
#     return await OperatorLicenseModel.find_all().to_list()