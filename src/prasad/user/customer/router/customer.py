from fastapi import APIRouter,status,HTTPException,Depends,File, UploadFile
from prasad.auth.model.user import UserModel
from prasad.auth.schemas.user import UserResponse
from prasad.images.model.image_model import ImageReason
from prasad.utils.user_info import get_user_info
from prasad.user.customer.model.customer import CustomerInfoModel,CustomerDetailsInfoModel,CustomerServicesDetailsModel
from prasad.user.customer.schemas.customer import CustomerInfoCreate, CustomerInfoDetailsCreate, \
    CustomerServicesDetailsCreate, CustomerInfoResponse, CustomerInfoDetailsResponse, CustomerServicesDetailsResponse
from prasad.images.image_services.image_services import ImageService



router = APIRouter(prefix="/customer", tags=["Customer"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerInfoCreate,file: UploadFile = File(...),user: dict = Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == user["user_id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.role != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="customer role not found")

    new_customer = CustomerInfoModel(
        user_id=db_user,
        first_name=customer.first_name,
        middle_name=customer.middle_name,
        last_name=customer.last_name,
        nickname=customer.nickname,
        phone=customer.phone,
        district=customer.district,
        mondal=customer.mondal,
        village=customer.village,
        registered_by=customer.registered_by
    )
    await new_customer.insert()
    metadata = {"user_id": str(db_user.id), "customer_id": str(new_customer.id)}

    # ✅ Step 5: Save image
    reason = ImageReason.PROFILE
    image_url = await ImageService().save_image_from_api(file, reason, metadata)

    # ✅ Step 6: Return response
    return {
        "message": "Customer created successfully",
        "customer_id": str(new_customer.id),
        "profile_image": image_url,
    }



@router.post("/details", status_code=status.HTTP_201_CREATED)
async def create_customer_details(customer_details: CustomerInfoDetailsCreate,user: dict = Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == user["user_id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.role=="customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="customer role not found")

    new_customer = CustomerDetailsInfoModel(
        user_id=db_user,
        kyc_number=customer_details.kyc_number,
        street=customer_details.street,
        city=customer_details.city,
        state=customer_details.state,
        postal_code=customer_details.postal_code,
        country=customer_details.country,
        industry=customer_details.industry,
        sub_industry=customer_details.sub_industry
    )
    await new_customer.insert()
    return {
        "message": "success",
    }




@router.post("/service_details", status_code=status.HTTP_201_CREATED)
async def create_customer_details(services_details: CustomerServicesDetailsCreate,user: dict = Depends(get_user_info)):
    db_user = await UserModel.find_one(UserModel.id == user["user_id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.role=="customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="customer role not found")

    new_customer_services_details = CustomerServicesDetailsModel(
        user_id=db_user,
        location_name=services_details.location_name,
        latitude_longitude=services_details.latitude_longitude,
        land_size=services_details.land_size,
        unit=services_details.unit,
        instructions=services_details.instructions,

    )
    await new_customer_services_details.insert()
    return {
        "message": "success",
    }





# @router.get("/details",status_code=status.HTTP_200_OK)
# async def get_all_customers_details():
#     customers_details =  await CustomerDetailsInfoModel.find_all().to_list()
#     return customers_details



#
# @router.get("/", status_code=status.HTTP_200_OK)
# async def get_all_customers():
#     db_users = await UserModel.find(UserModel.role=="customer").to_list()
#     response = []
#
#     for db_user in db_users:
#         user_res = UserResponse(**db_user.model_dump())
#
#         db_customer_info = await CustomerInfoModel.find_one(
#             CustomerInfoModel.user_id["id"] == db_user.id
#         )
#         db_customer_info_res = (
#             CustomerInfoResponse(**db_customer_info.model_dump())
#             if db_customer_info
#             else None
#         )
#
#         db_customer_info_details = await CustomerDetailsInfoModel.find_one(
#             CustomerDetailsInfoModel.user_id["id"] == db_user.id
#         )
#         db_customer_info_details_res = (
#             CustomerInfoDetailsResponse(**db_customer_info_details.model_dump())
#             if db_customer_info_details
#             else None
#         )
#
#         db_customer_services = await CustomerServicesDetailsModel.find_one(
#             CustomerServicesDetailsModel.user_id["id"] == db_user.id
#         )
#         db_customer_services_res = (
#             CustomerServicesDetailsResponse(**db_customer_services.model_dump())
#             if db_customer_services
#             else None
#         )
#
#         customer_data = {
#             "customer": user_res,
#             "customer_info": db_customer_info_res,
#             "customer_details": db_customer_info_details_res,
#             "customer_services": db_customer_services_res,
#         }
#
#         response.append(customer_data)
#
#     return response
#




# @router.get("/services_details",status_code=status.HTTP_200_OK)
# async def get_all_customers_services_details():
#     customers_services_details =  await CustomerServicesDetailsModel.find_all().to_list()
#     return customers_services_details

