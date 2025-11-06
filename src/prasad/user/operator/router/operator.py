from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.auth.schemas.user import UserResponse
from prasad.utils.user_info import get_user_info
from prasad.user.operator.model.operator import OperatorInfoModel
from prasad.user.operator.schemas.operator import OperatorInfoCreate, OperatorInfoResponse

router = APIRouter(prefix="/operator", tags=["Drone Operator"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_operator(operator_info: OperatorInfoCreate,user: dict = Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == user["user_id"])
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not db_user.role=="operator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator role not found")

    new_operator = OperatorInfoModel(
        user_id=db_user,
        first_name=operator_info.first_name,
        last_name=operator_info.last_name,
        phone_number=operator_info.phone_number,
        latitude_longitude=operator_info.latitude_longitude,
        service_radius=operator_info.service_radius,
        industry=operator_info.industry,
        sub_industry=operator_info.sub_industry
    )
    await new_operator.insert()
    return new_operator

#
# @router.get("/",status_code=status.HTTP_200_OK)
# async def get_all_operators():
#     db_users = await UserModel.find(UserModel.role=="operator").to_list()
#     response = []
#
#
#     for db_user in db_users:
#         user_res = UserResponse(**db_user.model_dump())
#         db_operator_info = await OperatorInfoModel.find_one(OperatorInfoModel.user_id["id"] == db_user.id)
#         db_operator_info_res= (
#             OperatorInfoResponse(**db_operator_info.model_dump())
#             if db_operator_info
#             else None
#         )
#         data={
#             "operator":user_res,
#             "operator_info":db_operator_info_res
#         }
#
#         response.append(data)
#
#     return response
#
