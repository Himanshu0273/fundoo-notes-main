import json
import os

from loguru import logger


class Logger:
    @staticmethod
    def initialize_from_json(config_path="logger_format.json"):
        logger.remove()

        def db_filter(record):
            return record.get("extra", {}).get("config", False)

        def func_filter(record):
            return record.get("extra", {}).get("func", False)
        
        def note_func_filter(record):
            return record.get("extra", {}).get("func1", False)

        abs_path = os.path.join(os.path.dirname(__file__), config_path)
        with open(abs_path, "r") as f:
            config_log = json.load(f)

        for handler in config_log["handlers"]:
            filter_name = handler.pop("filter", None)
            filter_func = {"config": db_filter, "func": func_filter, "func1": note_func_filter}.get(filter_name)

            logger.add(**handler, filter=filter_func)

        logger.info("Logger initialized from JSON config.")
        return logger


config_logger = Logger.initialize_from_json().bind(config=True)
func_logger = Logger.initialize_from_json().bind(func=True)
note_func_logger = Logger.initialize_from_json().bind(func1=True)
