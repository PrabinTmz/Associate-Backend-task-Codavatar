from fastapi import APIRouter

from api.v1.endpoints import auth, phonenumber

API_BASE_URL = "/api/v1"

api_router = APIRouter()

api_router.include_router(auth.router, prefix=f"{API_BASE_URL}/auth", tags=["auth"])

api_router.include_router(phonenumber.router, prefix=f"{API_BASE_URL}/phonenumbers", tags=["phonenumbers"])
