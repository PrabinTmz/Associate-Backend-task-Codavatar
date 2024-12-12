from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Dict

from core.config import settings


# General expiration times
TOKEN_EXPIRE_TIMES = {
    "access": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    "refresh": timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
}

# Secret key and algorithm for JWT
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.ALGORITHM


# Create JWT tokens with proper type embedded
async def create_token(data: dict, token_type: str) -> str:
    """
    Creates a JWT token with expiration and type claims.

    Args:
        data (dict): Data to encode in the token payload.
        token_type (str): Type of token to generate ('access' or 'refresh').

    Returns:
        str: Encoded JWT token.
    """
    expire_delta = TOKEN_EXPIRE_TIMES[token_type]
    # Calculate expiration time for the token
    expire = datetime.now(timezone.utc) + expire_delta

    # Embed expiration time and token type into the token payload
    data.update({"exp": expire, "type": token_type})

    # Encode the token using the provided secret key and algorithm
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    # Return the encoded JWT token
    return token


# Token verification with type checking
async def verify_token(token: str, token_type: str = "access") -> dict:
    """
    Verifies the provided JWT token and ensures it's of the expected type.

    Args:
        token (str): JWT token to verify.
        token_type (str): Expected token type ('access' or 'refresh').

    Returns:
        dict: Decoded payload of the token if valid.

    Raises:
        HTTPException: If token verification fails or token type mismatches.
    """
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Ensure the token type matches the expected type
        if payload.get("type") != token_type:
            raise JWTError("Invalid token type!")

        # Return the decoded payload if valid
        return payload
    except JWTError:
        # Raise an HTTP exception if token verification fails
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token!",
        )


async def generate_tokens(data: dict, token_type: str = "") -> Dict[str, str]:
    """
    Generates both or mentioned access and/or refresh tokens asynchronously.

    Args:
        data (dict): Data to encode in the tokens' payloads.
        token_type (str): access or refresh , by default "" for both

    Returns:
        Dict[str, str]: Dictionary containing the generated access, refresh tokens, auth type
    """

    token_dict = {"auth_type": "bearer"}

    # generate from mentioned token_type
    if token_type in ["access", "refresh"]:
        token_dict[f"{token_type}_token"] = await create_token(data, token_type)

    # generate both tokens
    elif token_type == "":
        token_dict["access_token"] = await create_token(data, "access")
        token_dict["refresh_token"] = await create_token(data, "refresh")

    return token_dict
