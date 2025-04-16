from fastapi import FastAPI
from config.conn_db import create_db_and_tables
from contextlib import asynccontextmanager
from routes.user_login import userlogin as login


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Generates and intializes new db with table"""
    yield create_db_and_tables()


app = FastAPI(lifespan=lifespan)

app.include_router(login, prefix="/login", tags=["Authentication"])
