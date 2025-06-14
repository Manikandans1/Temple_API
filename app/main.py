from fastapi import FastAPI
from app.api.admin.admin_routes import router as admin_router
from app.api.admin.temples import router as temple_router
from app.api.admin.services import router as service_router
from app.api.user.user_routes import router as user_router
from app.db.database import Base, engine
from app.api.admin.booking import router as booking_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import secrets


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

Base.metadata.create_all(bind=engine)


app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(temple_router, prefix="/admin/temple", tags=["Admin Temple Management"])
app.include_router(service_router, prefix="/admin/temple/service", tags=["Admin Temple Service Management"])
app.include_router(booking_router, prefix="/api", tags=["User Temple Booking"])
# app.include_router(booking_service, prefix="/api",tags=["Admin Temple Temple Service Management"])