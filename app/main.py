from fastapi import FastAPI, HTTPException

from api.v1 import auth, phonenumber


app = FastAPI()

API_BASE_URL = "/api/v1"

app.include_router(auth.router, prefix=f"{API_BASE_URL}/auth", tags=["auth"])
# app.include_router(phonenumber.router, prefix=f"{API_BASE_URL}/phonenumber", tags=["phonenumber"])


# Example Health check endpoint (useful for monitoring and load balancing)
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "FastAPI App is running."}

# Example Root endpoint (optional)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the PhoneNumber App!"}
