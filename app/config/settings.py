import os

from dotenv import load_dotenv

load_dotenv()


class DbSettings:

    # DB Credentials
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")


# All settings related to fastapi
class AppSettings:
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    APP_RELOAD = os.getenv("APP_RELOAD", "False").lower() == "true"


dbsettings = DbSettings()
appsettings = AppSettings()