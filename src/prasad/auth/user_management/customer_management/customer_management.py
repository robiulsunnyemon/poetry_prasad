from fastapi import APIRouter, HTTPException,status
from prasad.auth.model.user import UserModel
from prasad.auth.schemas.user import UserResponse
from prasad.user.customer.model.customer import CustomerInfoModel, CustomerDetailsInfoModel, CustomerServicesDetailsModel
from prasad.user.customer.schemas.customer import CustomerInfoResponse, CustomerInfoDetailsResponse,CustomerServicesDetailsResponse





router = APIRouter(
    prefix="/user/customer",
    tags=["Customer Management"],
)






@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_customers():
    db_users = await UserModel.find(UserModel.role=="customer").to_list()
    response = []

    for db_user in db_users:
        user_res = UserResponse(**db_user.model_dump())

        db_customer_info = await CustomerInfoModel.find_one(
            CustomerInfoModel.user_id["id"] == db_user.id
        )
        db_customer_info_res = (
            CustomerInfoResponse(**db_customer_info.model_dump())
            if db_customer_info
            else None
        )

        db_customer_info_details = await CustomerDetailsInfoModel.find_one(
            CustomerDetailsInfoModel.user_id["id"] == db_user.id
        )
        db_customer_info_details_res = (
            CustomerInfoDetailsResponse(**db_customer_info_details.model_dump())
            if db_customer_info_details
            else None
        )

        db_customer_services = await CustomerServicesDetailsModel.find_one(
            CustomerServicesDetailsModel.user_id["id"] == db_user.id
        )
        db_customer_services_res = (
            CustomerServicesDetailsResponse(**db_customer_services.model_dump())
            if db_customer_services
            else None
        )

        customer_data = {
            "customer": user_res,
            "customer_info": db_customer_info_res,
            "customer_details": db_customer_info_details_res,
            "customer_services": db_customer_services_res,
        }

        response.append(customer_data)

    return response




@router.get("/all_active", status_code=status.HTTP_200_OK)
async def get_all_active_customers():
    db_users = await UserModel.find({
        "role": "customer",
        "account_status": "active"
    }).to_list()

    response = []

    for db_user in db_users:
        user_res = UserResponse(**db_user.model_dump())

        db_customer_info = await CustomerInfoModel.find_one(
            CustomerInfoModel.user_id["id"] == db_user.id
        )
        db_customer_info_res = (
            CustomerInfoResponse(**db_customer_info.model_dump())
            if db_customer_info
            else None
        )

        db_customer_info_details = await CustomerDetailsInfoModel.find_one(
            CustomerDetailsInfoModel.user_id["id"] == db_user.id
        )
        db_customer_info_details_res = (
            CustomerInfoDetailsResponse(**db_customer_info_details.model_dump())
            if db_customer_info_details
            else None
        )

        db_customer_services = await CustomerServicesDetailsModel.find_one(
            CustomerServicesDetailsModel.user_id["id"] == db_user.id
        )
        db_customer_services_res = (
            CustomerServicesDetailsResponse(**db_customer_services.model_dump())
            if db_customer_services
            else None
        )

        customer_data = {
            "customer": user_res,
            "customer_info": db_customer_info_res,
            "customer_details": db_customer_info_details_res,
            "customer_services": db_customer_services_res,
        }

        response.append(customer_data)

    return response


@router.get("/all_pending", status_code=status.HTTP_200_OK)
async def get_all_pending_customers():
    db_users = await UserModel.find({
        "role": "customer",
        "account_status": "pending"
    }).to_list()

    response = []

    for db_user in db_users:
        user_res = UserResponse(**db_user.model_dump())

        db_customer_info = await CustomerInfoModel.find_one(
            CustomerInfoModel.user_id["id"] == db_user.id
        )
        db_customer_info_res = (
            CustomerInfoResponse(**db_customer_info.model_dump())
            if db_customer_info
            else None
        )

        db_customer_info_details = await CustomerDetailsInfoModel.find_one(
            CustomerDetailsInfoModel.user_id["id"] == db_user.id
        )
        db_customer_info_details_res = (
            CustomerInfoDetailsResponse(**db_customer_info_details.model_dump())
            if db_customer_info_details
            else None
        )

        db_customer_services = await CustomerServicesDetailsModel.find_one(
            CustomerServicesDetailsModel.user_id["id"] == db_user.id
        )
        db_customer_services_res = (
            CustomerServicesDetailsResponse(**db_customer_services.model_dump())
            if db_customer_services
            else None
        )

        customer_data = {
            "customer": user_res,
            "customer_info": db_customer_info_res,
            "customer_details": db_customer_info_details_res,
            "customer_services": db_customer_services_res,
        }

        response.append(customer_data)

    return response


@router.post("/do_suspend/${user_id}", status_code=status.HTTP_200_OK)
async def do_suspend_account(user_id:str):
    db_user = await UserModel.get(user_id)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if not db_user.otp_status == "verified":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Your account is not active or has expired")
    db_user.account_status = "suspended"
    await db_user.save()
    return {"message":"you have suspended successfully"}



@router.post("/do_active/${user_id}", status_code=status.HTTP_200_OK)
async def do_active_account(user_id:str):
    db_user = await UserModel.get(user_id)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if not db_user.otp_status == "verified":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Your account is not active or has expired")
    db_user.account_status = "active"
    await db_user.save()
    return {"message":"you have active successfully"}




@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customers_by_id(customer_id:str):
    db_user = await UserModel.find_one(UserModel.id==customer_id)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if not db_user.role == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not customer")


    user_res = UserResponse(**db_user.model_dump())

    db_customer_info = await CustomerInfoModel.find_one(
        CustomerInfoModel.user_id["id"] == db_user.id
    )
    db_customer_info_res = (
        CustomerInfoResponse(**db_customer_info.model_dump())
        if db_customer_info
        else None
    )

    db_customer_info_details = await CustomerDetailsInfoModel.find_one(
        CustomerDetailsInfoModel.user_id["id"] == db_user.id
    )
    db_customer_info_details_res = (
        CustomerInfoDetailsResponse(**db_customer_info_details.model_dump())
        if db_customer_info_details
        else None
    )

    db_customer_services = await CustomerServicesDetailsModel.find_one(
        CustomerServicesDetailsModel.user_id["id"] == db_user.id
    )
    db_customer_services_res = (
        CustomerServicesDetailsResponse(**db_customer_services.model_dump())
        if db_customer_services
        else None
    )

    customer_data = {
        "customer": user_res,
        "customer_info": db_customer_info_res,
        "customer_details": db_customer_info_details_res,
        "customer_services": db_customer_services_res,
    }



    return customer_data



