
from pydantic import Field, BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean
from . import database     

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # primary key and indexed
    username = Column(String, unique=False, index=True, nullable=False) # got to be unique, can be null
    email = Column(String, unique=True, index=True, nullable=True) # got to be unique, can be null
    hashed_password = Column(String, nullable=False) # can't null, ought to be a string

    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserOutPut(BaseModel):
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: str
    password: str
