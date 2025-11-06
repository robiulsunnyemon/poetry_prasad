from fastapi import FastAPI
from prasad.db.db import init_db, drop_user_collection
from prasad.auth.routers.authentication import router as auth_router
from prasad.auth.user_management.user_management import router as user_router
from prasad.auth.profile.profile import router as profile_router
from prasad.user.customer.router.customer import router as customer_router
from prasad.user.operator.router.operator import router as operator_router
from prasad.drone_details.routers.drone_details import router as drone_details_router
from prasad.equipment_details.routers.equipement_services import router as equipment_router
from prasad.license.router.license import router as license_router
from prasad.experience_record.routers.experience_record import router as experience_record_router
from prasad.services.drone_services.router.drone_services import router as drone_services_router
from prasad.industry.router.industry import router as industry_router
from fastapi.middleware.cors import CORSMiddleware
from prasad.auth.user_management.customer_management.customer_management import router as customer_user_router
from prasad.auth.user_management.operator_management.operator_management import router as operator_user_router
from prasad.order.drone_services_order.router.drone_services_order import router as drone_services_order_router
from fastapi.staticfiles import StaticFiles
from prasad.images.image_router.image_router import router as image_router

app = FastAPI(
    title="Prasad",
    version="1.0",
    description="Prasad",
)



origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://prasad.mtscorporate.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await  init_db()

@app.get("/",tags=["Root"])
async def root():
    return {"message": "Hello Prasad"}

@app.delete("/drop-collection",tags=["Drop Collection"])
async def drop_collection():
    await drop_user_collection()
    return {"message": "Collection dropped successfully"}



# Static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



### routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(profile_router)
app.include_router(customer_router)
app.include_router(operator_router)
app.include_router(drone_details_router)
app.include_router(equipment_router)
app.include_router(license_router)
app.include_router(experience_record_router)
app.include_router(drone_services_router)
app.include_router(industry_router)
app.include_router(customer_user_router)
app.include_router(operator_user_router)
app.include_router(drone_services_order_router)
app.include_router(image_router)