from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password utility
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password utility
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
