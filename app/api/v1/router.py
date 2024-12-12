from fastapi import APIRouter

from api.v1.endpoints import auth, phonenumber


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(phonenumber.router, prefix="/phonenumbers", tags=["phonenumbers"])
