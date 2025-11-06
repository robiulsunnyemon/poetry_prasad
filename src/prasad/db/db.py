from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie
from prasad.auth.model.user import UserModel
from prasad.drone_details.model.drone_details import DroneDetailsModel
from prasad.equipment_details.model.equipement_services import EquipmentHistoryModel
from prasad.experience_record.model.experience_record import OperatorRecordModel
from prasad.images.model.image_model import ImageModel
from prasad.industry.model.industry import SubIndustryModel, IndustryModel
from prasad.license.model.license import OperatorLicenseModel
from prasad.order.drone_services_order.model.drone_services_order import DroneServiceOrderModel
from prasad.services.drone_services.model.drone_service import DroneServiceModel
from prasad.user.customer.model.customer import CustomerInfoModel, CustomerDetailsInfoModel, CustomerServicesDetailsModel
from prasad.user.operator.model.operator import OperatorInfoModel
import os

MONGO_DETAILS = "mongodb://localhost:27017/prasad"

#
# load_dotenv()
#
# MONGO_DETAILS = os.getenv("MONGO_URI")

async def init_db():
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_DETAILS)
    database: AsyncIOMotorDatabase = client.get_database()

    # Beanie init
    await init_beanie(
        database=database,
        document_models=[
            UserModel,
            CustomerInfoModel,
            OperatorInfoModel,
            DroneDetailsModel,
            EquipmentHistoryModel,
            OperatorLicenseModel,
            OperatorRecordModel,
            CustomerDetailsInfoModel,
            CustomerServicesDetailsModel,
            DroneServiceModel,
            IndustryModel,
            SubIndustryModel,
            DroneServiceOrderModel,
            ImageModel
        ],
    )


async def drop_user_collection():
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_DETAILS)
    database: AsyncIOMotorDatabase = client.get_database()
    await database.drop_collection("drone_service_order")

