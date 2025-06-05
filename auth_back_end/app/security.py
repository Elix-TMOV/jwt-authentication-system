from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from .models import User
from sqlalchemy.orm import Session
from . import database

from fastapi import Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "secret"
ENCRYPTION_ALGO = "HS256"

# Create a password context using bcrypt.
password_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token with an expiration time.
    
    :param subject: The subject or identifier for the token (usually the user ID or email).
    :param expires_delta: Optional timedelta for token expiration.
    :return: A JWT token as a string.
    """
    # Calculate the expiration time.
    duration = expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + duration

    # Prepare the payload with expiration and subject.
    token_payload = {"exp": expire, "sub": subject}
    
    # Encode the payload into a JWT token.
    encoded_jwt = jwt.encode(token_payload, SECRET_KEY, algorithm=ENCRYPTION_ALGO)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the stored hashed password.
    
    :param plain_password: The password entered by the user.
    :param hashed_password: The hashed password stored in the database.
    :return: True if the password matches, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hashed password from a plain text password.
    
    :param password: The plain text password.
    :return: A securely hashed password.
    """
    return password_context.hash(password)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> User:
    """
    return the user associated with jwt token
    
    token: jwt token passed in the http header, it is extracted by the OAuth2PasswordBearer helper function
    
    """
    
    # print(request.headers, "here are the headers") # print the headers
    
    # print(token, 'here is the token by the user')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
   
        # try to decode the payload if there is an error doing it, raise exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ENCRYPTION_ALGO])
        
        # Get the user_id from the payload subject claim
        user_email = payload.get("sub")
        print('payload sub', user_email)
        if user_email is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception
    
    # find the user with the user email provided
  
    user = db.query(User).filter(User.email== user_email).first()
    if user is None:
        raise credentials_exception
    return user
            
    
    
