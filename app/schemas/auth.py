from pydantic import BaseModel, EmailStr


# Schema for token response containing access and refresh tokens
class Token(BaseModel):
    """
    Pydantic model for token response including access and refresh tokens
    with an authentication type identifier.
    """

    access_token: str  # JWT access token
    refresh_token: str  # JWT refresh token
    auth_type: str  # Token type, e.g., 'bearer'


# Schema specifically for token refresh request
class TokenRefresh(BaseModel):
    """
    Pydantic model to validate a refresh token in a token refresh request.
    """

    refresh_token: str


# Schema specifically for access token response
class TokenAccess(BaseModel):
    """
    Pydantic model for providing access token information to clients.
    """

    access_token: str
    auth_type: str


# Schema for creating a new user account with email and password
class UserCreate(BaseModel):
    """
    Pydantic model for user registration. Ensures email is valid and a password is provided.
    """

    email: EmailStr  # Validated email address
    password: str


# Schema for user login authentication request
class UserLogin(BaseModel):
    """
    Pydantic model to handle user login by validating provided email and password.
    """

    email: str
    password: str
