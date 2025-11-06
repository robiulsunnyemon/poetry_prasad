from fastapi import APIRouter,status,HTTPException,Depends
from prasad.auth.model.user import UserModel
from prasad.utils.user_info import get_user_info
from prasad.experience_record.model.experience_record import OperatorRecordModel
from prasad.experience_record.schemas.experience_record import OperatorRecordCreate


router = APIRouter(prefix="/experience_record", tags=["Experience Records"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_operator_record_experience(operator_record: OperatorRecordCreate,user:dict=Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id==user["user_id"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if not db_user.role=="operator":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your are not drone operator")

    new_operator_record=OperatorRecordModel(
        user_id=db_user,
        total_flight_hours=operator_record.total_flight_hours,
        past_project_and_events=operator_record.past_project_and_events,
    )
    await new_operator_record.insert()
    return new_operator_record



# @router.get("/",status_code=status.HTTP_200_OK)
# async def read_all_operator_records():
#     return await OperatorRecordModel.find_all().to_list()