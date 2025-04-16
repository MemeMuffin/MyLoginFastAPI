from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.routing import APIRouter
from sqlmodel import Session, select
from fastapi import Query, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user_login import User, UserCreate, UserPublic, UserUpdate, Token
from config.conn_db import get_session
from dependencies.user_login_dependencies import verify_password
from routes.utils import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_user,
    get_password_hash,
)


userlogin = APIRouter()


@userlogin.post("/register", response_model=UserPublic)
async def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """Registers New User"""
    db_user = get_user(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, name=user.name, age=user.age, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@userlogin.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]
):
    """Generates JWT token for user"""
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@userlogin.get("/login/me/", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Returns curret active authenticated user"""
    return current_user


@userlogin.get("/login/users/", response_model=list[UserPublic])
async def get_all_users(session: Annotated[Session, Depends(get_session)]):
    """Returns users stored in the database"""
    statement = select(User)
    users = session.exec(statement).all()
    return users


@userlogin.patch("/login/userupdate/", response_model=UserPublic)
async def update_exsisting_user(
    user: UserUpdate,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Updates user data within the database with new data given by user"""
    update_user = user.model_dump(exclude_unset=True)
    for key, value in update_user.items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@userlogin.patch("/login/passwordreset/", response_model=UserPublic)
async def reseting_exsisting_user_password(
    new_password: str,
    old_password: str,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Resets user password stored within database with new given password"""
    if not verify_password(old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    else:
        new_password = get_password_hash(new_password)
        current_user.password = new_password
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user
