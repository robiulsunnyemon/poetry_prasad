from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.auth.schemas.user import UserResponse
from prasad.utils.user_info import get_user_info
from prasad.equipment_details.model.equipement_services import EquipmentHistoryModel
from prasad.equipment_details.schemas.equipement_services import EquipmentCreate, EquipmentResponse

router = APIRouter(prefix="/equipments", tags=["Equipments Service"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_equipment_details(equipment: EquipmentCreate,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not drone operator")

    new_equipment = EquipmentHistoryModel(
        user_id=db_user,
        equipment_id=equipment.equipment_id,
        asset_id=equipment.asset_id,
        equipment_type=equipment.equipment_type,
        model=equipment.model,
        make=equipment.make,
        manufacturer=equipment.manufacturer,
        year=equipment.year,
        serial_number=equipment.serial_number,
        last_maintenance_date=equipment.last_maintenance_date
    )

    await new_equipment.insert()
    return {"equipment": new_equipment}



@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_equipments_history():
    equipments = await EquipmentHistoryModel.find().to_list()
    return {"equipments": equipments}


@router.get("/operator/{user_id}", status_code=status.HTTP_200_OK)
async def get_all_equipments_history(user_id:str):
    db_user = await UserModel.find_one(UserModel.id==user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not drone operator")

    equipments = await EquipmentHistoryModel.find(EquipmentHistoryModel.user_id["id"] == user_id).to_list()
    response=[]
    for equipment in equipments:
        data=(
            EquipmentResponse(**equipment.model_dump())
            if equipment
            else None
        )
        response.append(data)
    return {
        "operator":(
            UserResponse(**db_user.model_dump())
            if db_user
            else None
        ),
        "equipments": response
    }