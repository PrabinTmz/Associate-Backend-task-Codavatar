from fastapi import FastAPI, HTTPException

from api.v1.router import api_router
from middlewares.api_log import APILogMiddleware


app = FastAPI()

app.add_middleware(APILogMiddleware)

app.include_router(api_router)


# Example Health check endpoint (useful for monitoring and load balancing)
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "FastAPI App is running."}


# Example Root endpoint (optional)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the PhoneNumber App!"}
