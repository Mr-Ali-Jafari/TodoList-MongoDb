# create jwt auth in fastapi
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
# load environment variables
from dotenv import load_dotenv
import os

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Create a JWT token
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a function to hash a password
def get_password_hash(password):
    return pwd_context.hash(password)

# Create a function to verify a password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create a function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow()
        to_encode.update({"exp": expire})
        ded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return ded_jwt
