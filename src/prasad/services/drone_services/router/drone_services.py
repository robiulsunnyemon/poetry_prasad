from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.utils.user_info import get_user_info
from prasad.services.drone_services.model.drone_service import DroneServiceModel
from prasad.services.drone_services.schemas.drone_services import DroneServicesCreate, DroneServicesResponse,DroneServicesUpdate
from typing import List



router = APIRouter(prefix="/drone_services", tags=["Drone Services"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_drone_services(drone_services: DroneServicesCreate,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not admin")

    new_drone_service = DroneServiceModel(
        user_id=db_user,
        service_title=drone_services.service_title,
        service_price=drone_services.service_price,
        industry=drone_services.industry,
        sub_industry=drone_services.sub_industry,
        service_description=drone_services.service_description,
        service_location=drone_services.service_location

    )

    await new_drone_service.insert()
    return {"message": "success"}


@router.get("/",response_model=List[DroneServicesResponse], status_code=status.HTTP_200_OK)
async def read_drone_services():
    return await DroneServiceModel.find().to_list()


@router.get("/{services_id}",response_model=DroneServicesResponse, status_code=status.HTTP_200_OK)
async def read_drone_services(services_id:str):
    service=await DroneServiceModel.find_one(DroneServiceModel.id==services_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service



@router.delete("/{services_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_drone_services(services_id:str,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not admin")

    db_service = await DroneServiceModel.find_one(DroneServiceModel.id==services_id)
    if db_service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    await db_service.delete()
    return {"message": "success"}



@router.patch("/{services_id}", status_code=status.HTTP_200_OK)
async def read_drone_services(service_data:DroneServicesUpdate,services_id:str,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not db_user.role=="admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not admin")

    db_service = await DroneServiceModel.find_one(DroneServiceModel.id==services_id)

    if db_service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")


    update_service_data=service_data.model_dump(exclude_unset=True)

    if not update_service_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    await db_service.set(update_service_data)

    return {"message": "success"}
