import os
from pydantic.v1 import BaseSettings
from uvicorn.config import LOGGING_CONFIG

DATABASE_URI = "postgresql://postgres:password@localhost/todaysmenu_db"
ENV_FILE = os.getenv("ENV_FILE", ".env")
MEDIA = os.getenv("MEDIA", 'media')


class APISettings(BaseSettings):
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    LOG_LEVEL = "info"
    LOG_PATH = ""
    SECRET_KEY = '4123ba225618b201d6ea33ccd2f28322'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    UPLOAD_DIR = MEDIA
    MAX_FILE_SIZE_MB = 5
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ENV_FILE

    @property
    def log_config(self):
        if not self.LOG_PATH:
            return LOGGING_CONFIG
        os.makedirs(self.LOG_PATH, exist_ok=True)
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "uvicorn_default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(asctime)s.%(msecs)03d] %(levelname)s %(name)s %(module)s.%(funcName)s():%(lineno)s - %(message)s",
                    "use_colors": None,
                },
                "uvicorn_access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": "%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "uvicorn_error": {
                    "formatter": "uvicorn_default",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": f"{self.LOG_PATH}/error.log",
                },
                "uvicorn_access": {
                    "formatter": "uvicorn_access",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": f"{self.LOG_PATH}/access.log",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["uvicorn_error"], "level": "INFO", "propagate": False},
                "uvicorn.error": {"handlers": ["uvicorn_error"], "level": "INFO"},
                "uvicorn.access": {"handlers": ["uvicorn_access"], "level": "INFO", "propagate": False},
            },
        }


api_settings = APISettings()
