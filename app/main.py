import uvicorn 
from app.config.settings import appsettings

if __name__ == "__main__":
    uvicorn.run(
        "app.fapi:fapi", 
        host=appsettings.APP_HOST,
        port=appsettings.APP_PORT,
        reload=appsettings.APP_RELOAD
    )
