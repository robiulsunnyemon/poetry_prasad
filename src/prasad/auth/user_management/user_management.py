from fastapi import APIRouter, HTTPException,status
from typing import List
from prasad.auth.model.user import UserModel
from prasad.auth.schemas.user import UserResponse, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["User Management"],
)



@router.get("/all_user",response_model= List[UserResponse] ,status_code=status.HTTP_200_OK)
async def read_users():
    db_users = await UserModel.find_all().to_list()
    if db_users is None:
        db_users = []
    return db_users



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




@router.get("/{user_id}",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id:str):
    db_user= await UserModel.find_one(UserModel.id==user_id)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return db_user

@router.patch("/{user_id}",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id:str,user_info:UserUpdate):
    db_user= await UserModel.find_one(UserModel.id==user_id)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    update_info=user_info.model_dump(exclude_unset=True)
    if not update_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No fields to update")

    await db_user.set(update_info)

    return db_user

