from fastapi import Request, HTTPException, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
# from jose import JWTError
from utils.jwt import verify_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, exempt_routes: list):
        super().__init__(app)
        self.exempt_routes = exempt_routes

    async def dispatch(self, request: Request, call_next):
        # Check if the request path is in the exempt routes
        if request.url.path in self.exempt_routes:
            # Skip the middleware logic for exempted routes
            response = await call_next(request)
        else:
            # Apply middleware logic (e.g., logging, authentication, etc.)
            # Example: You can add custom logic here before calling the route handler
            token = request.headers.get("Authorization")
            if token:
                if token.startswith("Bearer "):
                    token = token[7:]  # Remove "Bearer " prefix
                else:
                    raise HTTPException(status_code=400, detail="Invalid token format")
                
                verify_access_token = verify_access_token(token)
                if verify_access_token is None:
                    raise HTTPException(status_code=401, detail="Invalid or expired token")
                
                # Attach user info to request state
                request.state.user = verify_access_token
                response = await call_next(request)
            else:
                raise HTTPException(status_code=401, detail="Please provide an access token!") # No authentication required for some routes
                response = await call_next(request)

        return response
