import sys

import uvicorn

from app.config.logger_config import Logger
from app.config.settings import appsettings
from app.utils.exceptions import RequiredEnvVarError

if __name__ == "__main__":
    # logger = Logger.initialize_from_json()
    try:
        uvicorn.run(
            "app.fapi:fapi",
            host=appsettings.APP_HOST,
            port=appsettings.APP_PORT,
            reload=appsettings.APP_RELOAD,
        )
    except RequiredEnvVarError as e:
        print(f"Configuration Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
