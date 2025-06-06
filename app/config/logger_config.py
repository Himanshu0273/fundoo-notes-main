import os
from loguru import logger
from pathlib import Path


class DBLogger:
    LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
    LOG_FILE = LOG_DIR / "db_log.log"
    
    
    @staticmethod
    def setup_logger():
        if not DBLogger.LOG_DIR.exists():
            DBLogger.LOG_DIR.mkdir(parents=True)
            
        logger.remove()
        
        logger.add(
            DBLogger.LOG_FILE,
            format=("{time:YYYY-MM-DD HH:mm:ss} | "
                "{level:<8} | "
                "{module:<15} | "
                "{message}"),
                
            level='DEBUG',
            rotation='1 MB',
            compression='zip',
            backtrace=True,
            diagnose=True                
        )
        
        logger.info("Logger initialized successfully!!!")
        
        return logger