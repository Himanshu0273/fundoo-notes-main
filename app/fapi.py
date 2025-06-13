from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import db_initialize
from app.config.logger_config import config_logger
from app.routers import auth, user, notes

# config_logger = logger.bind(func=True)


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        config_logger.info("🚀 App is starting up...")
        db_initialize.DbInitialize.create_tables()
        config_logger.info("📍 Database tables checked/created successfully!!!")
    except Exception as e:
        config_logger.exception(f"❌ Error in the startup stage: {e}")
    yield
    print("🙏 App shutting down...")

fapi = FastAPI(lifespan=lifespan)

# Router Registration
fapi.include_router(user.signup_router)
fapi.include_router(auth.auth_router)
fapi.include_router(user.user_router)
fapi.include_router(notes.notes_router)
