from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.auth.schemas.user import UserResponse
from prasad.utils.user_info import get_user_info
from prasad.drone_details.schemas.drone_details import DroneDetailsCreate,DroneDetailsResponse
from prasad.drone_details.model.drone_details import DroneDetailsModel


router = APIRouter(prefix="/drone_details", tags=["Drone Details"])
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_drone_details(drone_details: DroneDetailsCreate,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not drone operator")
    new_drone_details = DroneDetailsModel(
        user_id=db_user,
        drone_uin_uk=drone_details.drone_uin_uk,
        services_capabilities=drone_details.services_capabilities,
        model=drone_details.model,
        make=drone_details.make,
        manufacturer_year=drone_details.manufacturer_year,
        serial_number=drone_details.serial_number,
        manufacturer=drone_details.manufacturer,
        flight_hours=drone_details.flight_hours,
        last_maintenance_date=drone_details.last_maintenance_date,
        insurance_status=drone_details.insurance_status,
        rent_status=drone_details.rent_status,
        operational_status=drone_details.operational_status,
        battery_type=drone_details.battery_type,
        battery_cycles=drone_details.battery_cycles,
        battery_capacity=drone_details.battery_capacity,
        drone_condition=drone_details.drone_condition
    )
    await new_drone_details.insert()
    return {"message":"success"}



@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_drone_details():
    drones = await DroneDetailsModel.find_all().to_list()
    response = []

    for drone in drones:
        user = await drone.user_id.fetch()
        db_user = await UserModel.find_one(UserModel.id == user.id)
        response.append({
            "operator":(
                UserResponse(**db_user.model_dump())
                if db_user
                else None
            ),
            "drones": (
                DroneDetailsResponse(**drone.model_dump())
                if drone
                else None
            ),
        })

    return response


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_my_drone_details(user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == user["user_id"])
    if db_user.role!="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not drone operator")
    db_drone_details= await DroneDetailsModel.find(DroneDetailsModel.user_id["id"] == user["user_id"]).to_list()

    response = []

    for drone in db_drone_details:
        drone_res=(
            DroneDetailsResponse(**drone.model_dump())
            if drone
            else None
        )
        response.append(drone_res)
    return {
        "operator":(
            UserResponse(**db_user.model_dump())
            if db_user
            else None
        ),
        "drones": response
    }


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_drone_details_by_user_id(user_id: str):
    db_user = await UserModel.find_one(UserModel.id == user_id)
    if db_user.role!="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not drone operator")
    db_drone_details= await DroneDetailsModel.find(DroneDetailsModel.user_id["id"] == user_id).to_list()

    response = []

    for drone in db_drone_details:
        drone_res=(
            DroneDetailsResponse(**drone.model_dump())
            if drone
            else None
        )
        response.append(drone_res)
    return {
        "operator":(
            UserResponse(**db_user.model_dump())
            if db_user
            else None
        ),
        "drones": response
    }