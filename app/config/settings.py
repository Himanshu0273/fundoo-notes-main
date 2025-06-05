import os

from dotenv import load_dotenv

load_dotenv()

class DbSettings:
    
    #DB Credentials
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    
    
#All settings related to fastapi
class Settings:
    pass



dbsettings = DbSettings()