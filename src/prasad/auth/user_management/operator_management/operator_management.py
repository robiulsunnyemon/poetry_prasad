from fastapi import APIRouter, HTTPException,status
from typing import List
from src.prasad.auth.model.user import UserModel
from src.prasad.auth.schemas.user import UserResponse
from src.prasad.experience_record.model.experience_record import OperatorRecordModel
from src.prasad.experience_record.schemas.experience_record import OperatorRecordResponse
from src.prasad.license.model.license import OperatorLicenseModel
from src.prasad.license.schemas.license import LicenseResponse
from src.prasad.user.operator.model.operator import OperatorInfoModel
from src.prasad.user.operator.schemas.operator import OperatorInfoResponse




router = APIRouter(
    prefix="/operator",
    tags=["Drone Operator Management"],
)




@router.get("/all",status_code=status.HTTP_200_OK)
async def get_all_operators():
    db_users = await UserModel.find(UserModel.role=="operator").to_list()
    if db_users is None:
        db_users = []
        return db_users
    response = []


    for db_user in db_users:
        user_res = UserResponse(**db_user.model_dump())
        db_operator_info = await OperatorInfoModel.find_one(OperatorInfoModel.user_id["id"] == db_user.id)
        db_operator_info_res= (
            OperatorInfoResponse(**db_operator_info.model_dump())
            if db_operator_info
            else None
        )
        db_operator_license=await OperatorLicenseModel.find_one(OperatorLicenseModel.user_id["id"]==db_user.id)
        db_operator_license_res=(
            LicenseResponse(**db_operator_license.model_dump())
            if db_operator_license
            else None
        )
        db_operator_record = await OperatorRecordModel.find_one(OperatorRecordModel.user_id["id"] == db_user.id)
        db_operator_record_res=(
            OperatorRecordResponse(**db_operator_record.model_dump())
            if db_operator_record
            else None
        )

        data={
            "operator":user_res,
            "operator_info":db_operator_info_res,
            "operator_license":db_operator_license_res,
            "operator_record":db_operator_record_res,
        }

        response.append(data)

    return response



@router.get("/all_pending",status_code=status.HTTP_200_OK)
async def get_all_pending_operators():
    db_users = await UserModel.find({
        "role": "operator",
        "account_status": "pending"
    }).to_list()
    if db_users is None:
        return []

    response = []

    for db_user in db_users:
        user_res = UserResponse(**db_user.model_dump())
        db_operator_info = await OperatorInfoModel.find_one(OperatorInfoModel.user_id["id"] == db_user.id)
        db_operator_info_res= (
            OperatorInfoResponse(**db_operator_info.model_dump())
            if db_operator_info
            else None
        )
        db_operator_license=await OperatorLicenseModel.find_one(OperatorLicenseModel.user_id["id"]==db_user.id)
        db_operator_license_res=(
            LicenseResponse(**db_operator_license.model_dump())
            if db_operator_license
            else None
        )
        db_operator_record = await OperatorRecordModel.find_one(OperatorRecordModel.user_id["id"] == db_user.id)
        db_operator_record_res=(
            OperatorRecordResponse(**db_operator_record.model_dump())
            if db_operator_record
            else None
        )

        data={
            "operator":user_res,
            "operator_info":db_operator_info_res,
            "operator_license":db_operator_license_res,
            "operator_record":db_operator_record_res,
        }

        response.append(data)

    return response




@router.get("/all_active",status_code=status.HTTP_200_OK)
async def get_all_active_operators():
    db_users = await UserModel.find({
        "role": "operator",
        "account_status": "active"
    }).to_list()
    if db_users is None:
        return []

    response = []

    for db_user in db_users:
        user_res = UserResponse(**db_user.model_dump())
        db_operator_info = await OperatorInfoModel.find_one(OperatorInfoModel.user_id["id"] == db_user.id)
        db_operator_info_res= (
            OperatorInfoResponse(**db_operator_info.model_dump())
            if db_operator_info
            else None
        )
        db_operator_license=await OperatorLicenseModel.find_one(OperatorLicenseModel.user_id["id"]==db_user.id)
        db_operator_license_res=(
            LicenseResponse(**db_operator_license.model_dump())
            if db_operator_license
            else None
        )
        db_operator_record = await OperatorRecordModel.find_one(OperatorRecordModel.user_id["id"] == db_user.id)
        db_operator_record_res=(
            OperatorRecordResponse(**db_operator_record.model_dump())
            if db_operator_record
            else None
        )

        data={
            "operator":user_res,
            "operator_info":db_operator_info_res,
            "operator_license":db_operator_license_res,
            "operator_record":db_operator_record_res,
        }

        response.append(data)

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



@router.get("/operator/{user_id}",status_code=status.HTTP_200_OK)
async def get_operator_by_id(user_id:str):
    db_user= await UserModel.find_one(UserModel.id==user_id)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not db_user.role == "operator":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not operator")



    user_res = UserResponse(**db_user.model_dump())
    db_operator_info = await OperatorInfoModel.find_one(OperatorInfoModel.user_id["id"] == db_user.id)
    db_operator_info_res= (
        OperatorInfoResponse(**db_operator_info.model_dump())
        if db_operator_info
        else None
    )
    db_operator_license=await OperatorLicenseModel.find_one(OperatorLicenseModel.user_id["id"]==db_user.id)
    db_operator_license_res=(
        LicenseResponse(**db_operator_license.model_dump())
        if db_operator_license
        else None
    )
    db_operator_record = await OperatorRecordModel.find_one(OperatorRecordModel.user_id["id"] == db_user.id)
    db_operator_record_res=(
        OperatorRecordResponse(**db_operator_record.model_dump())
        if db_operator_record
        else None
    )

    data={
        "operator":user_res,
        "operator_info":db_operator_info_res,
        "operator_license":db_operator_license_res,
        "operator_record":db_operator_record_res,
    }



    return data



