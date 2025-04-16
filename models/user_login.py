from typing import Annotated
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from passlib.context import CryptContext


class UserBase(SQLModel):
    """General sqlmodel for users"""
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str | None = Field(index=True)
    name: str | None = Field(default=None)
    age: int | None = Field(default=None)
    disabled: bool = Field(default=False)


class User(UserBase, table=True):
    """General Table for user data stored within the database"""
    password: str | None = Field(index=True)


class UserPublic(UserBase):
    """Returns user data sotred within database without showing password"""
    id: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    """Model to create new users within database"""
    email: str
    name: str
    age: int
    disabled: bool
    password: str


class UserUpdate(BaseModel):
    """Model to update user data stored within database"""
    email: str | None = None
    name: str | None = None
    age: int | None = None
    disabled: bool | None = False



class Token(BaseModel):
    """Model to make JWT token for user authentication"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for token data"""
    username: str | None = None
