from fastapi import APIRouter, HTTPException,status,Depends
from prasad.auth.model.user import UserModel
from prasad.user.customer.schemas.customer import CustomerInfoResponse, CustomerInfoDetailsResponse, \
    CustomerServicesDetailsResponse
from prasad.user.operator.model.operator import OperatorInfoModel
from prasad.user.operator.schemas.operator import OperatorInfoResponse
from prasad.utils.user_info import get_user_info
from prasad.user.customer.model.customer import CustomerInfoModel,CustomerDetailsInfoModel,CustomerServicesDetailsModel
from prasad.auth.schemas.user import UserResponse

router = APIRouter(
    prefix="/profile",
    tags=["Profile Management"],
)



@router.get("/customer/me", status_code=status.HTTP_200_OK)
async def read_users(user: dict = Depends(get_user_info)):

    db_user = await UserModel.find_one(UserModel.email == user["email"])
    if db_user is None:
        raise HTTPException(status_code=404, detail="You are not registered")

    user_res= UserResponse(**db_user.model_dump())

    user_info_res = None
    user_info_details_res = None
    user_info_service_details_res = None


    if db_user.role == "customer":

        user_info = await CustomerInfoModel.find_one(CustomerInfoModel.user_id['id'] == user["user_id"])
        if user_info:
            user_info_res = CustomerInfoResponse(**user_info.model_dump())


        user_info_details = await CustomerDetailsInfoModel.find_one(
            CustomerDetailsInfoModel.user_id['id'] == user["user_id"]
        )
        if user_info_details:
            user_info_details_res = CustomerInfoDetailsResponse(**user_info_details.model_dump())


        user_info_service_details = await CustomerServicesDetailsModel.find_one(
            CustomerServicesDetailsModel.user_id['id'] == user["user_id"]
        )
        if user_info_service_details:
            user_info_service_details_res = CustomerServicesDetailsResponse(**user_info_service_details.model_dump())


    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not customer")

    return {
        "user": user_res,
        "user_info": user_info_res,
        "user_details": user_info_details_res,
        "user_service_details": user_info_service_details_res,
    }



@router.get("/operator/me", status_code=status.HTTP_200_OK)
async def read_users_for_operator(user: dict = Depends(get_user_info)):

    db_user = await UserModel.find_one(UserModel.email == user["email"])
    if not db_user.role == "operator":
        raise HTTPException(status_code=404, detail="You are not operator")

    db_user_res= UserResponse(**db_user.model_dump())
    if db_user is None:
        raise HTTPException(status_code=404, detail="You are not registered")

    db_user_info = await OperatorInfoModel.find_one(OperatorInfoModel.user_id["id"] == user["user_id"])
    db_user_info_res = OperatorInfoResponse(**db_user_info.model_dump())

    return {
        "user": db_user_res,
        "user_info": db_user_info_res,
    }
