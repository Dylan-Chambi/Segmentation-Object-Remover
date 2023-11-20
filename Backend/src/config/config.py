from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="Backend/.env")
    
    api_name: str = "Image Background Remover API"
    revision: str = "local"
    yolo_version: str = "yolov8m.pt" # El modelo a cargar debe estar en Backend/src/tf_models/
    log_level: str = "DEBUG"


@cache
def get_settings():
    return Settings()