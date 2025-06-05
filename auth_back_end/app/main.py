# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .security import create_access_token, get_current_user, verify_password, get_password_hash
from . import database

from .models import User, UserCreate, UserOutPut, UserLogin




# 2) Dependency: get_db from database.py
get_db = database.get_db

# 3) On startup, create the database tables (for demo only).

@asynccontextmanager
async def life_span(app: FastAPI):
    database.Base.metadata.create_all(bind=database.engine)
    yield
    
app = FastAPI(lifespan=life_span)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],            # list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # allow all headers
)



@app.get("/home")
def home():
    return JSONResponse(content="Hello World")

@app.post("/register", response_model=UserOutPut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user:
    1. Verify email is not already taken.
    2. Hash the password.
    3. Create the user in the DB.
    4. Return the created user (excluding password fields).
    """

    # Check if user already exists. get the first user with the given username
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password
    hashed_pw = get_password_hash(user_data.password)

    # Create User ORM object
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_pw)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # loads generated id and other fields
    except IntegrityError:
        db.rollback()
        # This can happen if two requests race in parallel and both pass the "existing_user" check.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered (race condition)",
        )

    # Return the user (Pydantic will use UserOut, so hashed_password is excluded)
    return new_user


@app.post("/login", response_model=UserOutPut)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
     
    # check if the user with this email exists or not
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    # time to verify the password against the stored hash for this email
    verify = verify_password(user_data.password, user.hashed_password)
    if not verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
        
    jwt_access_token = create_access_token(subject = user.email)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"username":user.username, "access_token": jwt_access_token, "token_type": "bearer"})

    
@app.get("/protected_route")
async def Protected_route(user: User = Depends(get_current_user)):
    # if the user jwt is invalid get_current_user function will throw an error
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"you are logged in. Your email is {user.email}, and bananas are berries"})

# @app.post("/delete_user")
# async def delete_user(user = Depends(get_current_user), db: Session = Depends(get_db)):
#     db.delete(user)
#     db.commit()
#     return