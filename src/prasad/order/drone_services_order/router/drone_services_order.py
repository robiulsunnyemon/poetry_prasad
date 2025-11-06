from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.schemas.user import UserResponse
from prasad.services.drone_services.model.drone_service import DroneServiceModel
from prasad.auth.model.user import UserModel
from prasad.order.drone_services_order.model.drone_services_order import DroneServiceOrderModel
from prasad.order.drone_services_order.schemas.drone_services_order import DroneServicesOrderCreate,DroneServicesOrderResponse
from prasad.services.drone_services.schemas.drone_services import DroneServicesResponse
from prasad.utils.user_info import get_user_info




router = APIRouter(prefix="/drone_services_order", tags=["Drone Services Order"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_drone_services_order(data: DroneServicesOrderCreate,user:dict=Depends(get_user_info)):
    user_id=user["user_id"]
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    db_user=await UserModel.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not db_user.role=="customer":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not a customer")

    db_services=await DroneServiceModel.get(data.drone_services_id)
    if db_services is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    new_drone_services_order = DroneServiceOrderModel(
        user_id=db_user,
        drone_services=db_services,
        service_date_time=data.service_date_time,
        service_location=data.service_location,
        order_status="pending",

    )

    await new_drone_services_order.insert()
    return new_drone_services_order



@router.get("/all", status_code=status.HTTP_200_OK)
async def read_drone_services_order_all():
    db_drone_services_orders= await DroneServiceOrderModel.find().to_list()
    response =[]
    for db_drone_services_order in db_drone_services_orders:
        service_user =await db_drone_services_order.user_id.fetch()
        db_user=await UserModel.find_one(UserModel.id==service_user.id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_res = UserResponse(**db_user.model_dump())
        drone_service= await db_drone_services_order.drone_services.fetch()
        db_drone_service =await DroneServiceModel.find_one(DroneServiceModel.id==drone_service.id)
        if db_drone_service is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        db_drone_service_res= DroneServicesResponse(**db_drone_service.model_dump())
        response.append({
            "order_id": db_drone_services_order.id,
            "user":user_res,
            "service_date_time": db_drone_services_order.service_date_time,
            "service_location": db_drone_services_order.service_location,
            "order_status": db_drone_services_order.order_status,
            "service": db_drone_service_res,


        })

    return response




@router.get("/", status_code=status.HTTP_200_OK)
async def read_drone_services_order():
    db_drone_services_orders= await DroneServiceOrderModel.find().to_list()
    return db_drone_services_orders




@router.get("/me", status_code=status.HTTP_200_OK)
async def read_drone_services_order(user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_res = UserResponse(**db_user.model_dump())
    db_drone_services_orders= await DroneServiceOrderModel.find(DroneServiceOrderModel.user_id.id==user["user_id"]).to_list()
    response =[]
    for db_drone_services_order in db_drone_services_orders:
        drone_service= await db_drone_services_order.drone_services.fetch()
        db_drone_service =await DroneServiceModel.find_one(DroneServiceModel.id==drone_service.id)
        if db_drone_service is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        db_drone_service_res= DroneServicesResponse(**db_drone_service.model_dump())
        response.append({
            "order_id": db_drone_services_order.id,
            "service": db_drone_service_res,
            "service_date_time": db_drone_services_order.service_date_time,
            "order_status": db_drone_services_order.order_status,
            "service_location": db_drone_services_order.service_location
        })

    return {
        "user": user_res,
        "orders":response
    }




@router.get("/{operator_id}", status_code=status.HTTP_200_OK)
async def read_drone_services_order_by_operator_id(operator_id:str,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == operator_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user["role"]!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")

    user_res = UserResponse(**db_user.model_dump())
    db_drone_services_orders= await DroneServiceOrderModel.find(DroneServiceOrderModel.user_id.id==operator_id).to_list()
    response =[]
    for db_drone_services_order in db_drone_services_orders:
        drone_service= await db_drone_services_order.drone_services.fetch()
        db_drone_service =await DroneServiceModel.find_one(DroneServiceModel.id==drone_service.id)
        if db_drone_service is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        db_drone_service_res= DroneServicesResponse(**db_drone_service.model_dump())
        response.append({
            "order_id": db_drone_services_order.id,
            "service": db_drone_service_res,
            "service_date_time": db_drone_services_order.service_date_time,
            "order_status": db_drone_services_order.order_status,
            "service_location": db_drone_services_order.service_location
        })

    return {
        "user": user_res,
        "orders":response
    }











