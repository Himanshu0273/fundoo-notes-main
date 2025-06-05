# from .config import settings
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.routers import user

from .config import db_initialize
from .database import get_db
from .models import user_model
from .schemas import user_schema
from .utils import hash

app = FastAPI()


# Runs the Load DB when the API Server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("App starting up...")
    db_initialize.DbInitialize.create_tables()
    yield
    # Shutdown logic
    print("App shutting down...")


# Router Registration
app.include_router(user.router)

# if __name__=="__main__":
# Setting ka object banna ke port aur URL lena aur yahi pe server run karna
