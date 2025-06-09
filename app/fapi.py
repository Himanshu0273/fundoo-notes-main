from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.logger_config import DBLogger
from app.routers import auth, user
from app.config import db_initialize

logger = DBLogger.setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    DBLogger.setup_logger()
    logger.info("🔧 Logger Setup Complete!!")
    try:
        logger.info("🚀 App is starting up...")
        db_initialize.DbInitialize.create_tables()
        logger.info("📍 Database tables checked/created successfully!!!")
    except Exception as e:
        logger.exception(f"❌ Error in the startup stage: {e}")
    yield
    print("🙏 App shutting down...")

fapi = FastAPI(lifespan=lifespan)

# Router Registration
fapi.include_router(user.router2)
fapi.include_router(auth.router)
fapi.include_router(user.router)
