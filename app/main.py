# from .config import settings
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.config.logger_config import DBLogger
from app.routers import auth, user

from .config import db_initialize
from .database import get_db
from .models import user_model
from .schemas import user_schema
from .utils import hash

logger = DBLogger.setup_logger()

# Runs the Load DB when the API Server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    DBLogger.setup_logger()
    logger.info("🔧 Logger Setup Complete!!")
    try:
        logger.info("🚀 App is starting up...")
        db_initialize.DbInitialize.create_tables()
        logger.info("💽 Database tables checked/created successfully!!!")
    
    except Exception as e:
        logger.exception(f"❌ Error in the startup stage: {e}")
    yield
    # Shutdown logic
    print("🙏 App shutting down...")

app = FastAPI(lifespan=lifespan)

# Router Registration
app.include_router(auth.router)
app.include_router(user.router)

# if __name__=="__main__":
# Setting ka object banna ke port aur URL lena aur yahi pe server run karna
