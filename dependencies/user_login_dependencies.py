import secrets, os
from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from config.conn_db import get_session
from models.user_login import pwd_context, User


SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password, hashed_password):
    """Verifies given password with stored password in the database"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hashes plain text password"""
    return pwd_context.hash(password)


def get_user(session: Session, email: str):
    """Returns current user info"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user
